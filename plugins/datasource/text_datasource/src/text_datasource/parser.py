from typing import List

from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node


def tokenize(text: str) -> List[str]:
    tokens = []
    current = []
    in_quotes = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_quotes:
            if ch == '\\' and i + 1 < len(text) and text[i + 1] == '"':
                current.append('"')
                i += 2
                continue
            elif ch == '"':
                in_quotes = False
            else:
                current.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch.isspace():
                if current:
                    tokens.append(''.join(current))
                    current = []
            else:
                current.append(ch)
        i += 1
    if current:
        tokens.append(''.join(current))
    return tokens


def build_graph(tokens: List[str], has_labels: bool, zero_based: bool, directed: bool, weighted: bool) -> Graph:
    tokens = list(tokens)

    def pop() -> str:
        if not tokens:
            raise ValueError("Unexpected end of input")
        return tokens.pop(0)

    n = int(pop())
    m = int(pop())

    offset = 0 if zero_based else 1

    if has_labels:
        labels = [pop() for _ in range(n)]
    else:
        labels = [str(i + (0 if zero_based else 1)) for i in range(n)]

    node_ids = [str(i + (0 if zero_based else 1)) for i in range(n)]
    nodes: dict = {}
    for i in range(n):
        node_id = node_ids[i]
        nodes[node_id] = Node(id=node_id, data={"label": labels[i]})

    edges = set()
    node_set = set(nodes.values())

    for _ in range(m):
        u_raw = int(pop())
        v_raw = int(pop())

        u_idx = u_raw - offset
        v_idx = v_raw - offset

        if not (0 <= u_idx < n and 0 <= v_idx < n):
            raise ValueError(f"Node index out of range: u={u_raw}, v={v_raw}")

        u_id = node_ids[u_idx]
        v_id = node_ids[v_idx]
        node_u = nodes[u_id]
        node_v = nodes[v_id]

        edge_data = {}
        if weighted:
            w_token = pop()
            try:
                edge_data["weight"] = int(w_token)
            except ValueError:
                edge_data["weight"] = float(w_token)

        edges.add(Edge(data=edge_data, src=node_u, target=node_v))
        if not directed:
            edges.add(Edge(data=edge_data, src=node_v, target=node_u))

    return Graph(edges=edges, nodes=node_set, directed=directed)
