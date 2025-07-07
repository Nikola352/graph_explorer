from typing import List

from core.use_cases.graph_context import GraphContext
from core.use_cases.plugin_recognition import load_plugins
from core.use_cases.workspaces import (get_workspace, get_workspaces,
                                       initialize_workspaces)


class Application(object):
    def __init__(self):
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

    def get_context(self) -> dict:
        return {
            "current_workspace_id": self.current_workspace_id,
            "workspaces": get_workspaces(),
            **self.graph_context.get_context()
        }

    def select_workspace(self, workspace_id: str):
        workspace = get_workspace(workspace_id)
        if workspace is not None:
            self.current_workspace_id = workspace_id
            self.graph_context = GraphContext(
                workspace,
                self.data_source_plugins,
                self.visualizer_plugins,
            )
