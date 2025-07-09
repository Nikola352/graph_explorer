from typing import Any, Dict, List

from core.use_cases.graph_context import GraphContext
from core.use_cases.plugin_recognition import load_plugins
from core.use_cases.workspaces import (get_workspace, get_workspaces,
                                       initialize_workspaces)


class Application(object):
    """
    Class that manages application state.
    The highest level operations should be initiated by calling methods on the Application object.
    All information for the current application state can be retrieved from here.
    """

    def __init__(self):
        """
        Initializes the Application object with default state.

        Loads available plugins, initializes workspaces, and creates a graph context
        for the first available workspace.
        """
        # Load available plugins
        self.data_source_plugins, self.visualizer_plugins = load_plugins()

        initialize_workspaces()
        workspace = get_workspaces()[0]
        self.current_workspace_id: str = workspace.id

        self.graph_context = GraphContext(
            workspace,
            self.data_source_plugins,
            self.visualizer_plugins,
        )

    def get_context(self) -> Dict[str, Any]:
        """
        Retrieves the complete application state context.

        :return: A dictionary containing:
            - current_workspace_id: ID of the active workspace
            - workspaces: List of all available workspaces
            - all the keys from the current graph context
        :rtype: dict[str, Any]
        """
        return {
            "current_workspace_id": self.current_workspace_id,
            "workspaces": get_workspaces(),
            **self.graph_context.get_context()
        }

    def select_workspace(self, workspace_id: str):
        """
        Changes the active workspace to the specified workspace.

        :param workspace_id: The ID of the workspace to activate.
        :type workspace_id: str
        :raises KeyError: If the specified workspace doesn't exist.
        """
        workspace = get_workspace(workspace_id)
        if workspace is None:
            raise KeyError("The workspace does not exist")
        self.current_workspace_id = workspace_id
        self.graph_context = GraphContext(
            workspace,
            self.data_source_plugins,
            self.visualizer_plugins,
        )
