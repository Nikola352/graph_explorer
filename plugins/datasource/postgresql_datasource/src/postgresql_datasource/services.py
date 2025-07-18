from typing import Dict, List, Set, Tuple

import psycopg2

from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node


def create_graph(host: str, port: int, database: str, username: str, password: str) -> Graph:
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    tables = _get_table_names(cursor)
    primary_keys = _get_primary_keys(cursor)

    nodes = {}
    table_columns: Dict[str, List[str]] = {}

    # 1. Create nodes
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()
        if cursor.description is None:
            continue
        columns = [col.name for col in cursor.description]
        table_columns[table] = columns  # cache columns

        # fallback: all columns as PK if no PK is set
        pk_columns = primary_keys.get(table, set(columns))

        for record in records:
            pk_values = [str(val) for val, col in zip(
                record, columns) if col in pk_columns]
            node_id = f"{table}:{'_'.join(pk_values)}"
            data = {col: val for col, val in zip(columns, record)}
            node = Node(id=node_id, data={"table": table, **data})
            nodes[node_id] = node

    # 2. Create edges via foreign keys
    fk_relations = _get_foreign_keys(cursor)
    edges = set()

    for src_table, fk_column, target_table, target_column in fk_relations:
        src_pk_cols = primary_keys.get(src_table)
        target_pk_cols = primary_keys.get(target_table)
        if not src_pk_cols or not target_pk_cols:
            continue

        query = f"""
            SELECT s.*, t.*
            FROM {src_table} s
            JOIN {target_table} t ON s.{fk_column} = t.{target_column}
        """
        cursor.execute(query)
        links = cursor.fetchall()

        src_cols = table_columns[src_table]
        tgt_cols = table_columns[target_table]

        src_col_count = len(src_cols)

        for link in links:
            src_values = link[:src_col_count]
            target_values = link[src_col_count:]

            src_pk_values = [str(val) for val, col in zip(
                src_values, src_cols) if col in src_pk_cols]
            target_pk_values = [str(val) for val, col in zip(
                target_values, tgt_cols) if col in src_pk_cols]

            src_node_id = f"{src_table}:{'_'.join(src_pk_values)}"
            target_node_id = f"{target_table}:{'_'.join(target_pk_values)}"

            src_node = nodes.get(src_node_id)
            target_node = nodes.get(target_node_id)

            if src_node and target_node:
                edge_data = {
                    "relation": f"{src_table}.{fk_column} -> {target_table}.{target_column}"
                }
                edge = Edge(data=edge_data, src=src_node, target=target_node)
                edges.add(edge)

    conn.close()

    return Graph(nodes=set(nodes.values()), edges=edges, directed=True)


def _get_table_names(cursor) -> List[str]:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    return [row[0] for row in cursor.fetchall()]


def _get_primary_keys(cursor) -> Dict[str, Set[str]]:
    """
    Get primary key columns for each table.
    Returns a dict: {table_name: [pk_column1, pk_column2, ...]}
    """
    cursor.execute("""
        SELECT
            kcu.table_name,
            kcu.column_name
        FROM
            information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_schema = 'public'
        ORDER BY kcu.ordinal_position
    """)
    pk_info = {}
    for table, column in cursor.fetchall():
        pk_info.setdefault(table, set()).add(column)
    return pk_info


def _get_foreign_keys(cursor) -> List[Dict]:
    """
    Get foreign key constraints between tables.
    Returns list of tuples: (source_table, fk_column, target_table, target_column)
    """
    cursor.execute("""
        SELECT
            tc.table_name AS source_table,
            kcu.column_name AS fk_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
        WHERE constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public'
    """)
    return cursor.fetchall()
