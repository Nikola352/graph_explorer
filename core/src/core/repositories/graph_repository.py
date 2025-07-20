from datetime import datetime
from typing import Dict, List, Optional, Tuple, cast

from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node
from core.models.filter import Filter
from neo4j import GraphDatabase, ManagedTransaction, Query, Result


class GraphRepository(object):
    """
    Class responsible for storing and retrieving graph data from a Neo4j database.
    """

    def __init__(self, uri: str, user: str, password: str):
        """
        Initializes the GraphRepository with database connection parameters.

        :param uri: Neo4j database URI
        :type uri: str
        :param user: Database username
        :type user: str
        :param password: Database password
        :type password: str
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._initialize_schema()

    def _initialize_schema(self):
        """
        Creates the necessary indexes to optimize query patterns in the current setup.
        """
        with self.driver.session() as session:
            # Create node index
            session.run("""
            CREATE INDEX node_id_graph_index IF NOT EXISTS
            FOR (n:Node) ON (n.id, n.graph_id)
            """)
            # Create relationship index
            session.run("""
            CREATE INDEX rel_graph_index IF NOT EXISTS
            FOR ()-[r:inRelationTo]-() ON (r.graph_id)
            """)

    def close(self):
        """
        Closes the database driver connection.
        """
        self.driver.close()

    def save_graph(self, id: str, graph: Graph):
        """
        Saves a graph to the database with the given ID.

        :param id: Unique identifier for the graph
        :type id: str
        :param graph: Graph object to be saved
        :type graph: Graph
        """
        with self.driver.session() as session:
            session.execute_write(self._save_graph, id, graph)

    def query_graph(self, id: str, filters: List[Filter], search_term: str = "") -> Graph:
        """
        Retrieves a graph from the database by its ID, optionally applying filters.

        :param id: Unique identifier of the graph to retrieve
        :type id: str
        :param filters: List of filters to apply (currently unused)
        :type filters: list
        :return: Retrieved Graph object
        :rtype: Graph
        """

        metadata_query = """
        MATCH (meta:GraphMeta {graph_id: $graph_id})
        RETURN meta
        """

        graph_query = """
        MATCH (n:Node {graph_id: $graph_id})
        {n_where_clause}
        OPTIONAL MATCH (n)-[r:inRelationTo {graph_id: $graph_id}]->(m:Node {graph_id: $graph_id})
        {m_where_clause}
        RETURN n, r, m
        """

        with self.driver.session() as session:
            result = session.run(metadata_query, graph_id=id)
            directed, root_id = self._parse_metadata(result)

            n_where_clause, params = self._build_where_clause(
                filters, search_term, "n")
            m_where_clause, params = self._build_where_clause(
                filters, search_term, "m")
            query = cast(Query, graph_query
                         .replace("{n_where_clause}", n_where_clause)
                         .replace("{m_where_clause}", m_where_clause)
                         )
            result = session.run(query, graph_id=id, **params)
            return self._parse_graph(result, directed, root_id)

    @staticmethod
    def _save_graph(tx: ManagedTransaction, graph_id: str, graph: Graph):
        # 1. Save graph metadata
        tx.run("""
            MERGE (meta:GraphMeta {graph_id: $graph_id})
            SET meta.directed = $directed,
                meta.root_id = $root_id,
                meta.updated_at = datetime()
        """, graph_id=graph_id, directed=graph.directed, root_id=graph.root_id)

        node_ids = [node.id for node in graph.nodes]

        # 2. Delete nodes not in the current list
        tx.run("""
            MATCH (n:Node {graph_id: $graph_id})
            WHERE NOT n.id IN $node_ids
            DETACH DELETE n
        """, graph_id=graph_id, node_ids=node_ids)

        # 3. Upsert nodes
        for node in graph.nodes:
            tx.run("""
                MERGE (n:Node {id: $id, graph_id: $graph_id})
                SET n = $props
            """, id=node.id, graph_id=graph_id, props={**node.data, "id": node.id, "graph_id": graph_id})

        # 4. Delete all edges for this graph (simpler and safer than trying to diff)
        tx.run("""
            MATCH (:Node {graph_id: $graph_id})-[r]->(:Node {graph_id: $graph_id})
            DELETE r
        """, graph_id=graph_id)

        # 5. Recreate all edges
        for edge in graph.edges:
            query = f"""
                MATCH (a:Node {{id: $from_id, graph_id: $graph_id}}),
                      (b:Node {{id: $to_id, graph_id: $graph_id}})
                MERGE (a)-[r:inRelationTo {{graph_id: $graph_id}}]->(b)
                SET r += $data
            """
            tx.run(query, from_id=edge.src.id, to_id=edge.target.id,
                   graph_id=graph_id, data=edge.data)

    @staticmethod
    def _parse_metadata(result: Result) -> Tuple[bool, Optional[str]]:
        for record in result:
            meta = record["meta"]
            if meta:
                directed = meta.get("directed", True)
                root_id = meta.get("root_id", None)
                return directed, root_id
        return True, None

    @staticmethod
    def _parse_graph(result: Result, directed: bool = True, root_id: Optional[str] = None) -> Graph:
        node_map: Dict[str, Node] = {}
        edges = set()

        for record in result:
            n_data = record["n"]
            m_data = record["m"]
            r_data = record["r"]

            # Node n
            n_id = n_data["id"]
            if n_id not in node_map:
                node_map[n_id] = Node(
                    id=n_id, data={k: v for k, v in n_data.items() if k != "id" and k != "graph_id"})
            n_node = node_map[n_id]

            # Node m
            if m_data:
                m_id = m_data["id"]
                if m_id not in node_map:
                    node_map[m_id] = Node(
                        id=m_id, data={k: v for k, v in m_data.items() if k != "id" and k != "graph_id"})
                m_node = node_map[m_id]

            # Edge
            if r_data:
                edge_data = {k: v for k, v in r_data.items() if k !=
                             "graph_id"}
                edge = Edge(data=edge_data, src=n_node, target=m_node)
                edges.add(edge)

        return Graph(nodes=set(node_map.values()), edges=edges, directed=directed, root_id=root_id)

    def _build_where_clause(self, filters: List[Filter], search_term: Optional[str], node_name: str) -> Tuple[str, Dict]:
        filter_clause, params = self._build_filter_clause(filters, node_name)
        clauses = [filter_clause]
        if search_term:
            search_clause, search_params = self._build_search_clause(
                search_term, node_name)
            clauses.append(search_clause)
            params.update(search_params)
        clause_str = " AND ".join([c for c in clauses if c.strip()])
        return "WHERE " + clause_str if clause_str else "", params

    @staticmethod
    def _build_filter_clause(filters: List[Filter], node_name: str) -> Tuple[str, Dict]:
        clauses = []
        params = {}

        for i, f in enumerate(filters):
            param_key = f"_param_{i}"
            if f.type == 'int' or f.type == 'float':
                params[param_key] = f.value
                clause = f"({node_name}.{f.field} {str(f.operator)} ${param_key})"
            elif f.type == 'datetime':
                date_value = cast(datetime, f.value)
                clause = f"({node_name}.{f.field} {str(f.operator)} date('{date_value.isoformat()}'))"
            else:  # str
                params[param_key] = f.value
                clause = f"({node_name}.{f.field} {str(f.operator)} ${param_key})"
            clauses.append(clause)

        return " AND ".join(clauses), params

    @staticmethod
    def _build_search_clause(search_term: str, node_name: str) -> Tuple[str, Dict]:
        search_term_key = "search_term"
        regex = f"(?i).*{search_term}.*"
        clause = f"ANY(prop IN keys({node_name}) WHERE {node_name}[prop] =~ ${search_term_key})"
        params = {search_term_key: regex}
        return clause, params