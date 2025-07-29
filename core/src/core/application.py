from typing import Any, Dict, List, Optional

from api.components.data_source import DataSourceConfigParam
from core.commands.command_names import CommandNames
from core.commands.command_processor import CommandProcessor
from core.commands.filter_commands import *
from core.commands.graph_commands import *
from core.commands.workspace_commands import *
from core.config.application_config import ApplicationConfig, load_app_config
from core.models.filterOperator import FilterOperator
from core.models.workspace import Workspace
from core.repositories.graph_repository.implementations.neo4j_graph_repository import \
    Neo4JGraphRepository
from core.repositories.workspace_repository.implementations.tiny_db_workspace_repository import \
    WorkspaceRepository
from core.use_cases.graph_context_factory import GraphContextFactory
from core.use_cases.plugin_recognition import load_plugins
from core.use_cases.workspace_context import WorkspaceContext
from core.use_cases.workspaces import WorkspaceService


class Application(object):
    """
    Class that manages application state.
    The highest level operations should be initiated by calling methods on the Application object.
    All information for the current application state can be retrieved from here.
    """

    def __init__(self, app_config: Optional[ApplicationConfig] = None):
        """
        Initializes the Application object with default state.

        Loads available plugins, initializes workspaces, and creates a graph context
        for the first available workspace.
        """
        if app_config is None:
            app_config = load_app_config()

        # Load available plugins
        self.data_source_plugins, self.visualizer_plugins = load_plugins()


        # Initializer workspace storage
        workspace_repo = WorkspaceRepository(app_config.workspace_db_path)
        self.workspace_service = WorkspaceService(workspace_repo)


        # Initializer graph storage
        self.graph_repository = Neo4JGraphRepository(
            uri=app_config.graph_db_uri,
            user=app_config.graph_db_user,
            password=app_config.graph_db_password
        )

        self.graph_context_factory = GraphContextFactory(
            self.workspace_service,
            self.graph_repository,
            self.data_source_plugins,
            self.visualizer_plugins
        )

        self.workspace_context = WorkspaceContext(
            self.workspace_service, self.graph_context_factory)

        self.command_processor = AppCommandProcessor(self)

    @property
    def graph_context(self) -> GraphContext:
        return self.workspace_context.graph_context

    def get_context(self) -> Dict[str, Any]:
        """
        Retrieves the complete application state context.

        :return: A dictionary containing:
            - current_workspace_id: ID of the active workspace
            - workspaces: List of all available workspaces
            - data_sources: Available data sources
            - visualizers: Available visualizers
            - all the keys from the current graph context
        :rtype: dict[str, Any]
        """
        return {
            "workspaces": self.workspace_service.get_workspaces(),
            "operators": FilterOperator.choices(),
            "data_sources": self.data_source_plugins,
            "visualizers": self.visualizer_plugins,
            **self.workspace_context.get_context()
        }

    def get_data_source_config_params(self, data_source_id: str) -> List[DataSourceConfigParam]:
        """
        Get the available configuration options for a given data source plugin.

        :param data_source_id: The ID of the data source.
        :type data_source_id: str
        :return: A list of available configuration parameters. An empty list if the data source is not found.
        :rtype: List[DataSourceConfigParam]
        """
        data_source = next(
            (ds for ds in self.data_source_plugins if ds.identifier() == data_source_id), None)
        if not data_source:
            return []
        return data_source.get_configuration_parameters()


class AppCommandProcessor(CommandProcessor):
    """Processor that manages and executes Graph Explorer commands."""

    def __init__(self, app: "Application"):
        super().__init__()
        self.app = app
        self._command_registry.update({
            CommandNames.CREATE_NODE: lambda args: CreateNodeCommand(app.graph_context, args),
            CommandNames.UPDATE_NODE: lambda args: UpdateNodeCommand(app.graph_context, args),
            CommandNames.DELETE_NODE: lambda args: DeleteNodeCommand(app.graph_context, args),
            CommandNames.CREATE_EDGE: lambda args: CreateEdgeCommand(app.graph_context, args),
            CommandNames.UPDATE_EDGE: lambda args: UpdateEdgeCommand(app.graph_context, args),
            CommandNames.DELETE_EDGE: lambda args: DeleteEdgeCommand(app.graph_context, args),
            CommandNames.CLEAR_GRAPH: lambda _: ClearGraphCommand(app.graph_context),
            CommandNames.SEARCH: lambda args: SearchCommand(app.graph_context, args),
            CommandNames.FILTER: lambda args: FilterCommand(app.graph_context, args),
            CommandNames.CLEAR_SEARCH: lambda _: ClearSearchCommand(app.graph_context),
            CommandNames.REMOVE_FILTER: lambda args: RemoveFilterCommand(app.graph_context, args),
            CommandNames.SELECT_WORKSPACE: lambda args: SelectWorkspaceCommand(app.workspace_context, args),
            CommandNames.CREATE_WORKSPACE: lambda args: CreateWorkspaceCommand(
                app.workspace_service,
                app.workspace_context,
                args
            ),
            CommandNames.UPDATE_WORKSPACE: lambda args: UpdateWorkspaceCommand(
                workspace_service=app.workspace_service,
                workspace_context=app.workspace_context,
                args=args,
            ),
            CommandNames.DELETE_WORKSPACE: lambda args: DeleteWorkspaceCommand(
                workspace_service=app.workspace_service,
                workspace_context=app.workspace_context,
                graph_repository=app.graph_repository,
                args=args
            ),
            CommandNames.SELECT_VISUALIZER: lambda args: SelectVisualizerCommand(
                graph_context=app.graph_context,
                find_visualizer_by_id=lambda id: app.graph_context_factory.visualizer_map[id],
                args=args,
            ),
            CommandNames.REFRESH_DATA_SOURCE: lambda args: RefreshDataSourceCommand(app.graph_context),
        })
