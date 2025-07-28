import json
from typing import Any, Dict, Tuple

from api.models.node import Node
from core.commands.command import Command
from core.use_cases.graph_context import GraphContext


class CreateNodeCommand(Command):
    """Command to create a new node."""

    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        super().__init__()
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        """
        Execute the create node command.

        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        node_id = self.args.get('id')
        data_arg = self.args.get('data', '{}')

        if not node_id:
            return False, 'Node ID is required.'

        try:
            graph = self.graph_context.get_graph()
        except KeyError:
            return False, "No graph context available"

        existing_node = next((n for n in graph.get_nodes()
                             if n.id == str(node_id)), None)
        if existing_node:
            return False, f'Node {node_id} already exists.'

        try:
            node_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'

        node = Node(str(node_id), node_data)
        graph.add_node(node)
        self.graph_context.save_graph(graph)
        return True, f'Node {node_id} created.'


class UpdateNodeCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        node_id = self.args.get('id')
        data_arg = self.args.get('data', '{}')

        if not node_id:
            return False, 'Node ID is required.'

        graph = self.graph_context.get_graph()
        node = next((n for n in graph.get_nodes()
                    if n.id == str(node_id)), None)
        if not node:
            return False, f'Node {node_id} not found.'

        try:
            node_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'

        graph.update_node(node, node_data)
        self.graph_context.save_graph(graph)
        return True, f'Node {node_id} updated.'


class UpdateEdgeCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        src_id = self.args.get('src')
        tgt_id = self.args.get('tgt')
        data_arg = self.args.get('data', '{}')

        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'

        graph = self.graph_context.get_graph()
        src = next((n for n in graph.get_nodes() if n.id == str(src_id)), None)
        tgt = next((n for n in graph.get_nodes() if n.id == str(tgt_id)), None)

        if not src or not tgt:
            return False, 'Both nodes must exist.'

        edge = next((e for e in graph.get_edges() if e.src.id ==
                    str(src_id) and e.target.id == str(tgt_id)), None)
        if not edge:
            return False, f'Edge {src_id} -> {tgt_id} not found.'

        try:
            edge_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'

        graph.update_edge(edge, edge_data)
        self.graph_context.save_graph(graph)
        return True, f'Edge {src_id} -> {tgt_id} updated.'


class DeleteNodeCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        node_id = self.args.get('id')
        if not node_id:
            return False, 'Node ID is required.'

        graph = self.graph_context.get_graph()
        node = next((n for n in graph.get_nodes()
                    if n.id == str(node_id)), None)
        if not node:
            return False, f'Node {node_id} not found.'

        graph.remove_node(node)
        self.graph_context.save_graph(graph)
        return True, f'Node {node_id} deleted.'


class CreateEdgeCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        src_id = self.args.get('src')
        tgt_id = self.args.get('tgt')
        data_arg = self.args.get('data', '{}')

        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'
        if src_id == tgt_id:
            return False, 'Recursive edges are not possible'

        graph = self.graph_context.get_graph()
        src = next((n for n in graph.get_nodes() if n.id == str(src_id)), None)
        tgt = next((n for n in graph.get_nodes() if n.id == str(tgt_id)), None)

        if not src or not tgt:
            return False, 'Both nodes must exist.'

        if any(e.src.id == str(src_id) and e.target.id == str(tgt_id) for e in graph.get_edges()):
            return False, 'Edge already exists.'

        try:
            edge_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'

        from api.models.edge import Edge
        edge = Edge(edge_data, src, tgt)
        graph.add_edge(edge)

        self.graph_context.save_graph(graph)

        return True, f'Edge {src_id} -> {tgt_id} created.'


class DeleteEdgeCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        src_id = self.args.get('src')
        tgt_id = self.args.get('tgt')

        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'

        graph = self.graph_context.get_graph()
        edge = next((e for e in graph.get_edges() if e.src.id ==
                    str(src_id) and e.target.id == str(tgt_id)), None)
        if not edge:
            return False, f'Edge {src_id} -> {tgt_id} not found.'

        graph.remove_edge(edge)
        self.graph_context.save_graph(graph)
        return True, f'Edge {src_id} -> {tgt_id} deleted.'


class ClearGraphCommand(Command):
    """Command to clear all nodes and edges from the graph."""

    def __init__(self, graph_context: GraphContext) -> None:
        self.graph_context = graph_context

    def execute(self) -> Tuple[bool, str]:
        graph = self.graph_context.get_graph()
        for node in list(graph.get_nodes()):
            graph.remove_node(node)
        self.graph_context.save_graph(graph)
        return True, 'Graph cleared.'
