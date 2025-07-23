from api.models.edge import Edge
from api.models.node import Node
from typing import Optional, Set
from api.models.data import OperatorMap

class Graph():
    """
    A class representing a graph structure composed of nodes and edges.

    :param edges: A set of edges in the graph.
    :type edges: set[Edge]
    :param nodes: A set of nodes in the graph.
    :type nodes: set[Node]
    :param directed: A boolean indicating whether the graph is directed.
    :type directed: boolean
    :param root_id: Identifier for the root node in the graph.
    :type root_id: str
    """

    def __init__(self, edges: Optional[Set[Edge]] = None, nodes: Optional[Set[Node]] = None, directed: Optional[bool] = True, root_id: Optional[str] = None):
        """
        Initializes a Graph object.

        :param edges: A set of edges to initialize the graph with. Defaults to None.
        :type edges: (set, optional) 
        :param nodes: A set of nodes to initialize the graph with. Defaults to None.
        :type node: (set, optional)
        :param directed: Indicates whether the graph is directed. Defaults to True.
        :type directed: (bool, optional)
        :param root_id: Identifier for the root node in the graph. Defaults to None.
        :type root_id: (str, optional)
        :return: Doesn't return anything but initializes `Graph` object.
        :rtype: None
        """
        super().__init__()
        self.edges = edges if edges else set()
        self.nodes = nodes if nodes else set()
        self.directed = directed
        self.root_id = root_id
        self.operator_map = OperatorMap()
        
        

    def add_node(self, node: Node) -> None:
        """
        Adds a `Node` to the graph.

        :param node:  The node to be added to the graph.
        :type node: `Node`
        """
        if not isinstance(node, Node):
            raise TypeError(
                f"Expected a Node instance, got {type(node).__name__}")
        self.nodes.add(node)

    def remove_node(self, target_node: Node) -> None:
        """
        Remove a `Node` to the graph and all adjecent edges.

        :param node:  The node to be added to the graph.
        :type node: `Node`
        """
        try:
            self.nodes.remove(target_node)
        except KeyError:
            raise ValueError(f"{target_node} not found in graph!")

        self.edges = set([edge for edge in self.edges if edge.src !=
                         target_node and edge.target != target_node])
        # remove edges from each node
        for node in self.nodes:
            node.edges = [
                edge for edge in node.edges if edge.src != target_node and edge.target != target_node
            ]

    def add_edge(self, edge: Edge) -> None:
        """
        Adds an `Edge` to the graph.

        :param node:  The node to be added to the graph.
        :type node: `Edge`
        """
        if not isinstance(edge, Edge):
            raise TypeError(
                f"Expected a Edge instance, got {type(edge).__name__}")
        self.nodes.add(edge.src)
        self.nodes.add(edge.target)
        if edge not in self.edges:
            self.edges.add(edge)

            if not self.directed:
                reversed_edge = Edge(edge.data, edge.target, edge.src)
                self.edges.add(reversed_edge)

            for node in self.nodes:
                if node == edge.src:
                    node.edges.append(edge)
                if not self.directed and node == edge.target:
                    node.edges.append(reversed_edge)

    def update_node(self, node: Node, data: dict) -> None:
        """
        Updates a `Node` in the graph.
        """
        if not isinstance(node, Node):
            raise TypeError(
                f"Expected a Node instance, got {type(node).__name__}")
        for n in self.nodes:
            if n.id == node.id:
                n.data = data
                break
            
    def update_edge(self, edge: Edge, data: dict) -> None:
        """
        Updates an `Edge` in the graph.
        """
        if not isinstance(edge, Edge):
            raise TypeError(
                f"Expected a Edge instance, got {type(edge).__name__}")
        
        for e in self.edges:
            if e.src == edge.src and e.target == edge.target:
                e.data = data
                break

    def remove_edge(self, target_edge: Edge) -> None:
        """
        Removes an `Edge` to the graph.

        :param node:  The node to be removed from the graph.
        :type node: `Edge`
        """
        

        if target_edge in self.edges:
            self.edges.remove(target_edge)

            if not self.directed:
                reversed_edge = Edge(
                    target_edge.data, target_edge.target, target_edge.src)
                self.edges.remove(reversed_edge)

            for node in self.nodes:
                if node == target_edge.src:
                    node.edges = [
                        edge for edge in node.edges if node != target_edge.src]
                if not self.directed and node == target_edge.target:
                    node.edges = [
                        edge for edge in node.edges if node != target_edge.target]
                    
    def search_nodes(self, query: str) -> Set[Node]:
        """
        Searches the graph for nodes containing the query string.
        """
        nodes = set()
        for node in self.nodes:
            for _, value in node.data.items():
                if query in str(value):
                    nodes.add(node)
        return nodes
    
    def search_edges(self, query: str) -> Set[Edge]:
        """
        Searches the graph for edges containing the query string.
        """
        edges = set()
        for edge in self.edges:
            for _, value in edge.data.items():
                if query in str(value):
                    edges.add(edge)
            for _, value in edge.src.data.items():
                if query in str(value):
                    edges.add(edge)
            for _, value in edge.target.data.items():
                if query in str(value):
                    edges.add(edge)
        return edges
    
    def filter_nodes(self, field: str, operator: str, param: str) -> Set[Node]:
        """
        Filters the graph for nodes containing the query string.
        """
        
        if operator not in self.operator_map.operators:
            raise ValueError(f"Unknown operator: {operator}")
        
        operator_func = self.operator_map.operators[operator]
        nodes = set()
        
        for node in self.nodes:
            if field in node.data and operator_func(node.data[field], type(node.data[field])(param)):
                nodes.add(node)
        return nodes
    
    def filter_edges(self, field: str, operator: str, param: str) -> Set[Edge]:
        """
        Filters the graph for edges containing the query string.
        """
        
        if operator not in self.operator_map.operators:
            raise ValueError(f"Unknown operator: {operator}")
        
        operator_func = self.operator_map.operators[operator]
        edges = set()
        
        for edge in self.edges:
            if field in edge.data and operator_func(edge.data[field], type(edge.data[field])(param)):
                edges.add(edge)
            if field in edge.src.data and operator_func(edge.src.data[field], type(edge.src.data[field])(param)):
                edges.add(edge)
            if field in edge.target.data and operator_func(edge.target.data[field], type(edge.target.data[field])(param)):
                edges.add(edge)
        return edges
    
    def get_nodes(self) -> Set["Node"]:
        """
        Retrieves all nodes in the graph.

        :return: A set containing all nodes in the graph.
        :rtype: set[`Node`]
        """
        return self.nodes

    def get_edges(self) -> Set["Edge"]:
        """
        Retrieves all edges in the graph.

        :return: A set containing all edges in the graph.
        :rtype: set[`Edge`]
        """
        return self.edges

    def __str__(self) -> str:
        graph = f"Graph(root_id: {self.root_id}, directed: {self.directed}, nodes_count: {len(self.nodes)}, edges_count: {len(self.edges)})"
        for node in self.nodes:
            graph += "\n\t" + node.__str__()
        return graph
