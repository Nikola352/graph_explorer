from abc import ABC, abstractmethod
from typing import Tuple, Any, Dict
import json
from api.models.graph import Graph
from core.models.filter import Filter
from core.models.filterOperator import FilterOperator
from django.apps import apps
from core.use_cases.graph_context import GraphContext


class GraphCommand(ABC):
    """Abstract base class for graph commands following Open/Closed principle."""
    
    @abstractmethod
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary of command arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        pass


class CreateNodeCommand(GraphCommand):
    """Command to create a new node."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the create node command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'id' and optional 'data' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        node_id = args.get('id') 
        data_arg = args.get('data', '{}')
        
        if not node_id:
            return False, 'Node ID is required.'
            
        existing_node = next((n for n in graph.get_nodes() if n.id == str(node_id)), None)
        if existing_node:
            return False, f'Node {node_id} already exists.'
            
        try:
            node_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'
            
        from api.models.node import Node
        node = Node(str(node_id), node_data)
        graph.add_node(node)
        return True, f'Node {node_id} created.'
    
class UpdateNodeCommand(GraphCommand):
    """Command to update a node."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the update node command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'id' and optional 'data' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        node_id = args.get('id')
        data_arg = args.get('data', '{}')
        
        if not node_id:
            return False, 'Node ID is required.'

        print("NODE ID", node_id)
        node = next((n for n in graph.get_nodes() if n.id == str(node_id)), None)
        if not node:
            return False, f'Node {node_id} not found.'
            
        try:
            node_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'
            
        graph.update_node(node, node_data)
        return True, f'Node {node_id} updated.'
    
class UpdateEdgeCommand(GraphCommand):
    """Command to update an edge."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the update edge command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'src', 'tgt' and optional 'data' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        src_id = args.get('src')
        tgt_id = args.get('tgt')
        data_arg = args.get('data', '{}')
        
        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'
        
        src = next((n for n in graph.get_nodes() if n.id == str(src_id)), None)
        tgt = next((n for n in graph.get_nodes() if n.id == str(tgt_id)), None)
        
        print("SRC", src)
        print("TGT", tgt)
        
        if not src or not tgt:
            return False, 'Both nodes must exist.'
        
        edge = next((e for e in graph.get_edges() if e.src.id == str(src_id) and e.target.id == str(tgt_id)), None)
        if not edge:
            return False, f'Edge {src_id} -> {tgt_id} not found.'
            
        try:
            edge_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'
        
        graph.update_edge(edge, edge_data)
        return True, f'Edge {src_id} -> {tgt_id} updated.'
    
class SearchCommand(GraphCommand):
    """Command to search the graph."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the search command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'query' argument
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        query = args.get('query')
        if not query:
            return False, 'Query is required.'
        
        graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context
        
        graph_context.search_term = query
        
        return True, f'Search query: {query}'
    
class FilterCommand(GraphCommand):
    """Command to filter the graph."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the filter command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'field', 'operator' and 'value' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context
        
        field = args.get('field')
        operator = args.get('operator')
        value = args.get('value')

        if not field or not operator or not value:
            return False, 'All filter parameters are required.'
                    
        filter = Filter(field=field, operator=FilterOperator(operator), value=value)
        graph_context.add_filter(filter)
        
        return True, f'Filter added: {filter}'
    

class DeleteNodeCommand(GraphCommand):
    """Command to delete a node."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the delete node command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'id' argument
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        node_id = args.get('id')  
        
        if not node_id:
            return False, 'Node ID is required.'
            
        node = next((n for n in graph.get_nodes() if n.id == str(node_id)), None)
        if not node:
            return False, f'Node {node_id} not found.'
            
        graph.remove_node(node)
        return True, f'Node {node_id} deleted.'


class CreateEdgeCommand(GraphCommand):
    """Command to create a new edge."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the create edge command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'src', 'tgt' and optional 'data' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        src_id = args.get('src')
        tgt_id = args.get('tgt')
        data_arg = args.get('data', '{}')
        
        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'
        if src_id == tgt_id:
            return False, 'Recursive edges are not possible'
            
        src = next((n for n in graph.get_nodes() if n.id == str(src_id)), None)
        tgt = next((n for n in graph.get_nodes() if n.id == str(tgt_id)), None)
        
        if not src or not tgt:
            return False, 'Both nodes must exist.'
            
        edgeCheck = next((e for e in graph.get_edges() if e.src.id == str(src_id) and e.target.id == str(tgt_id)), None)
        if edgeCheck:
            return False, 'Edge already exists.'
            
        try:
            edge_data = json.loads(data_arg) if data_arg else {}
        except Exception:
            return False, f'Invalid JSON format: {data_arg}'
            
        from api.models.edge import Edge
        edge = Edge(edge_data, src, tgt)
        graph.add_edge(edge)
        return True, f'Edge {src_id} -> {tgt_id} created.'


class DeleteEdgeCommand(GraphCommand):
    """Command to delete an edge."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the delete edge command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary containing 'src' and 'tgt' arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        src_id = args.get('src')
        tgt_id = args.get('tgt')
        
        if not src_id or not tgt_id:
            return False, 'Both source and target node IDs are required.'
            
        edge = next((e for e in graph.get_edges() if e.src.id == str(src_id) and e.target.id == str(tgt_id)), None)
        
        if not edge:
            return False, f'Edge {src_id} -> {tgt_id} not found.'
            
        graph.remove_edge(edge)
        return True, f'Edge {src_id} -> {tgt_id} deleted.'


class ClearGraphCommand(GraphCommand):
    """Command to clear all nodes and edges from the graph."""
    
    def execute(self, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute the clear graph command.
        
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary of command arguments (not used for this command)
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        for node in list(graph.get_nodes()):
            graph.remove_node(node)
            
        return True, 'Graph cleared.'


class GraphCommandProcessor:
    """Processor that manages and executes graph commands."""
    
    def __init__(self):
        self._commands = {
            'create-node': CreateNodeCommand(),
            'delete-node': DeleteNodeCommand(),
            'create-edge': CreateEdgeCommand(),
            'delete-edge': DeleteEdgeCommand(),
            'clear-graph': ClearGraphCommand(),
            'update-node': UpdateNodeCommand(),
            'update-edge': UpdateEdgeCommand(),
            'search': SearchCommand(),
            'filter': FilterCommand(),
        }
    
    def register_command(self, command_name: str, command: GraphCommand) -> None:
        """
        Register a new command.
        
        :param command_name: The name of the command to register
        :type command_name: str
        :param command: The command instance to register
        :type command: GraphCommand
        
        :return: None
        :rtype: None
        """
        self._commands[command_name] = command
    
    def execute_command(self, command_name: str, graph: Graph, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Execute a command by name.
        
        :param command_name: The name of the command to execute
        :type command_name: str
        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary of command arguments
        :type args: Dict[str, Any]
        
        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        if command_name not in self._commands:
            return False, f'Unknown command: {command_name}'
        
        command = self._commands[command_name]
        return command.execute(graph, args) 