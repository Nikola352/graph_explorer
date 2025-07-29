from core.models.workspace import Workspace
from core.use_cases.graph_context_factory import GraphContextFactory
from core.use_cases.workspaces import WorkspaceService


class WorkspaceContext(object):
    def __init__(self, workspace_service: WorkspaceService, context_factory: GraphContextFactory):
        self.workspace_service = workspace_service
        self.graph_context_factory = context_factory

        workspace = self.workspace_service.get_workspaces()[0]
        self.current_workspace_id: str = workspace.id

        self.graph_context = self.graph_context_factory.make(workspace)

    def get_context(self) -> dict:
        return {
            "current_workspace_id": self.current_workspace_id,
            **self.graph_context.get_context()
        }

    def select_workspace(self, workspace_id: str, refresh: bool = False) -> Workspace:
        """
        Changes the active workspace to the specified workspace.

        :param workspace_id: The ID of the workspace to activate.
        :type workspace_id: str
        :param refresh: Whether to load new data from the data source after selection.
        :type refresh: bool
        :raises KeyError: If the specified workspace doesn't exist.
        """
        workspace = self.workspace_service.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError("The workspace does not exist")
        self.current_workspace_id = workspace_id

        self.graph_context = self.graph_context_factory.make(workspace)

        if refresh:
            self.graph_context.refresh_data_source()

        return workspace

    def is_last(self) -> bool:
        return len(self.workspace_service.get_workspaces()) <= 1

    def select_first_workspace(self):
        workspace = self.workspace_service.get_workspaces()[0]
        self.select_workspace(workspace.id)
