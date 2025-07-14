from typing import Any, Dict, List, Optional

from core.config.application_config import ApplicationConfig, load_app_config
from core.models.filterOperator import FilterOperator
from core.models.workspace import Workspace
from core.repositories.graph_repository import GraphRepository
from core.repositories.workspace_repository import WorkspaceRepository
from core.use_cases.graph_context import GraphContext
from core.use_cases.plugin_recognition import load_plugins
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
        workspace = self.workspace_service.get_workspaces()[0]
        self.current_workspace_id: str = workspace.id

        # Initializer graph storage
        self.graph_repository = GraphRepository(
            uri=app_config.graph_db_uri,
            user=app_config.graph_db_user,
            password=app_config.graph_db_password
        )

        # Create the initial graph context
        self.graph_context = GraphContext(
            workspace,
            self.data_source_plugins,
            self.visualizer_plugins,
            self.workspace_service,
            self.graph_repository,
        )

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
            "current_workspace_id": self.current_workspace_id,
            "workspaces": self.workspace_service.get_workspaces(),
            "operators": FilterOperator.choices(),
            "data_sources": self.data_source_plugins,
            "visualizers": self.visualizer_plugins,
            **self.graph_context.get_context()
        }

    def select_workspace(self, workspace_id: str) -> Workspace:
        """
        Changes the active workspace to the specified workspace.

        :param workspace_id: The ID of the workspace to activate.
        :type workspace_id: str
        :raises KeyError: If the specified workspace doesn't exist.
        """
        workspace = self.workspace_service.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError("The workspace does not exist")
        self.current_workspace_id = workspace_id
        self.graph_context = GraphContext(
            workspace,
            self.data_source_plugins,
            self.visualizer_plugins,
            self.workspace_service,
            self.graph_repository,
        )
        return workspace
