import json

from django.apps import apps
from django.core.management.base import BaseCommand

from core.application import Application
from core.commands.command_names import CommandNames
from core.commands.command_processor import CommandProcessor
from core.use_cases.workspace_context import WorkspaceContext


def process_graph_command(subcommand, args_dict):
    """
    Process graph commands using the new command processor interface.
    
    :param subcommand: The command to execute (e.g., 'create-node', 'delete-edge')
    :type subcomand: string
    :param args_dict: Dictionary of command arguments
    :type args_dict: Dictionary
        
    :return: Tuple of success and message
    :rtype: Tuple(bool, string)
    """
    workspace_context: WorkspaceContext = apps.get_app_config(
        'graph_explorer').workspace_context  # type: ignore
    
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    workspace_id = args_dict.get('workspace')
    if workspace_id:
        try:
            workspace_context.select_workspace(str(workspace_id))
        except Exception as e:
            return False, f'Failed to select workspace {workspace_id}: {str(e)}'
    
    graph_context = workspace_context.graph_context
    if not graph_context:
        return False, 'No graph context available. Please select a workspace first.'

    success, message = processor.execute_command(subcommand, args_dict)
    
    return success, message


class Command(BaseCommand):
    """
    Class responsible for execute command line instructions on workspaces.
    
    JSON Format Usage:
    When using JSON data in command line, you must escape quotes properly:
    - Use: '{\"name\": \"Test\"}' 
    - NOT: '{"name": "Test"}' (this will cause parsing errors)
    
    Examples:
    - create-node --workspace <id> --id 1 --data '{\"name\": \"John\", \"age\": 30}'
    - create-edge --workspace <id> --src 1 --tgt 2 --data '{\"weight\": 5, \"type\": \"friendship\"}'

    NOTICE:
    - locate in graph_explorer/graph_explorer and type "python manage.py graph_cli <ONE_OF_EXAMPLES_ABOVE>" 
    """
    help = 'Graph CLI commands for node and edge manipulation. Use escaped JSON format: \'{\\"name\\": \\"Test\\"}\''

    def add_arguments(self, parser):
        """
        Add command line arguments to the parser.
        
        :param parser: The argument parser to add arguments to
        :type parser: argparse.ArgumentParser
        
        :return: None
        :rtype: None
        """
        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Create node command
        create_node_parser = subparsers.add_parser(
            CommandNames.CREATE_NODE, help='Create a new node')
        create_node_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        create_node_parser.add_argument('--id', type=str, required=True, help='Node ID')
        create_node_parser.add_argument('--data', type=str, default='{}', 
                                      help='Node data as JSON (use escaped format: \'{\\"name\\": \\"Test\\"}\')')
        
        # Update node command
        update_node_parser = subparsers.add_parser(
            CommandNames.UPDATE_NODE, help='Update a node')
        update_node_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        update_node_parser.add_argument('--id', type=str, required=True, help='Node ID')
        update_node_parser.add_argument('--data', type=str, default='{}', 
                                      help='Node data as JSON (use escaped format: \'{\\"name\\": \\"Test\\"}\')')
        
        # Update edge command
        update_edge_parser = subparsers.add_parser(
            CommandNames.UPDATE_EDGE, help='Update an edge')
        update_edge_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        update_edge_parser.add_argument('--src', type=str, required=True, help='Source node ID')
        update_edge_parser.add_argument('--tgt', type=str, required=True, help='Target node ID')
        update_edge_parser.add_argument('--data', type=str, default='{}', 
                                      help='Edge data as JSON (use escaped format: \'{\\"weight\\": 5}\')')
        
        # Delete node command
        delete_node_parser = subparsers.add_parser(
            CommandNames.DELETE_NODE, help='Delete a node')
        delete_node_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        delete_node_parser.add_argument('--id', type=str, required=True, help='Node ID')
        
        # Create edge command
        create_edge_parser = subparsers.add_parser(
            CommandNames.CREATE_EDGE, help='Create a new edge')
        create_edge_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        create_edge_parser.add_argument('--src', type=str, required=True, help='Source node ID')
        create_edge_parser.add_argument('--tgt', type=str, required=True, help='Target node ID')
        create_edge_parser.add_argument('--data', type=str, default='{}', 
                                      help='Edge data as JSON (use escaped format: \'{\\"weight\\": 5}\')')
        
        # Delete edge command
        delete_edge_parser = subparsers.add_parser(
            CommandNames.DELETE_EDGE, help='Delete an edge')
        delete_edge_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        delete_edge_parser.add_argument('--src', type=str, required=True, help='Source node ID')
        delete_edge_parser.add_argument('--tgt', type=str, required=True, help='Target node ID')
        
        # Search command
        search_parser = subparsers.add_parser(
            CommandNames.SEARCH, help='Search the graph')
        search_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        search_parser.add_argument('--query', type=str, required=True, help='Search query')
        
        # Filter command
        filter_parser = subparsers.add_parser(
            CommandNames.FILTER, help='Filter the graph')
        filter_parser.add_argument('--workspace', type=str, help='Workspace ID to use')
        filter_parser.add_argument('--field', type=str, required=True, help='Field to filter')
        filter_parser.add_argument('--operator', type=str, required=True, help='Filter operator')
        filter_parser.add_argument('--value', type=str, required=True, help='Filter value')
        
        # Clear graph command
        clear_graph_parser = subparsers.add_parser(
            CommandNames.CLEAR_GRAPH, help='Clear all nodes and edges from the graph')
        clear_graph_parser.add_argument('--workspace', type=str, help='Workspace ID to use')

    def handle(self, *args, **options):
        """
        Handle the command execution.
        
        :param args: Additional arguments passed to the command
        :type args: tuple
        :param options: Dictionary of command options and arguments
        :type options: dict
        
        :return: None
        :rtype: None
        """
        command = options.get('command')
        if not command:
            self.stdout.write('ERROR: No command specified.')
            self.stdout.write('\nJSON Format Examples:')
            self.stdout.write('  create-node --id 1 --data \'{\\"name\\": \\"Test\\"}\'')
            self.stdout.write('  create-edge --src 1 --tgt 2 --data \'{\\"weight\\": 5}\'')
            return
        
        args_dict = {k: v for k, v in options.items() if k != 'command' and v is not None}
        
        success, message = process_graph_command(command, args_dict)
        
        if success:
            self.stdout.write(f'SUCCESS: {message}')
        else:
            self.stdout.write(f'ERROR: {message}') 