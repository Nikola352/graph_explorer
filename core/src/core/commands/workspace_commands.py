from typing import Any, Callable, Dict, Tuple

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.commands.command import Command
from core.models.workspace import Workspace
from core.repositories.graph_repository.interfaces.base_graph_repository import \
    BaseGraphRepository
from core.use_cases.graph_context import GraphContext
from core.use_cases.workspaces import WorkspaceService


class SelectWorkspaceCommand(Command):
    def __init__(self, select_workspace: Callable[[str], Workspace], args: Dict[str, Any]) -> None:
        self.select_workspace = select_workspace
        self.workspace_id = str(args["workspace_id"])

    def execute(self) -> Tuple[bool, str]:
        workspace = self.select_workspace(self.workspace_id)
        return True, f"Selected workspace {workspace.name}"


class CreateWorkspaceCommand(Command):
    def __init__(self, workspace_service: WorkspaceService, select_workspace: Callable[[str, bool], Workspace], args: Dict[str, Any]) -> None:
        self.workspace_service = workspace_service
        self.select_workspace = select_workspace
        self.name = args.get("name")
        self.data_source_id = args.get("data_source_id")
        self.config = args.get("config", {})

    def execute(self) -> Tuple[bool, str]:
        if not self.name:
            return False, "Missing 'name'"
        if not self.data_source_id:
            return False, "Missing 'data source'"

        try:
            workspace = self.workspace_service.create_workspace(
                self.name, self.data_source_id, self.config)
            self.select_workspace(workspace.id, True)
            return True, f"Created {workspace.name}"
        except Exception as e:
            return False, f"Failed to create workspace: {str(e)}"


class UpdateWorkspaceCommand(Command):
    def __init__(self,
                 workspace_service: WorkspaceService,
                 select_workspace: Callable[[str, bool], Workspace],
                 args: Dict[str, Any],
                 ):
        self.workspace_service = workspace_service
        self.select_workspace = select_workspace
        self.workspace_id = args.get("workspace_id")
        self.name = args.get("name")
        self.data_source_id = args.get("data_source_id")
        self.config = args.get("config", {})

    def execute(self) -> Tuple[bool, str]:
        if not self.workspace_id:
            return False, "Missing 'workspace_id'"
        if not self.name:
            return False, "Missing 'name'"
        if not self.data_source_id:
            return False, "Missing 'data source'"

        try:
            workspace = self.workspace_service.update(
                str(self.workspace_id), self.name, self.data_source_id, self.config)
            self.select_workspace(workspace.id, True)

            return True, f"Updated {workspace.name}"
        except KeyError:
            return False, f"Workspace not found: {self.workspace_id}"
        except Exception as e:
            return False, f"Failed to update workspace: {str(e)}"


class DeleteWorkspaceCommand(Command):
    def __init__(self,
                 workspace_service: WorkspaceService,
                 graph_repository: BaseGraphRepository,
                 args: Dict[str, Any]
                 ) -> None:
        self.workspace_service = workspace_service
        self.graph_repository = graph_repository
        self.workspace_id = args.get("workspace_id")

    def execute(self) -> Tuple[bool, str]:
        if not self.workspace_id:
            return False, "Missing 'workspace_id'"

        try:
            self.workspace_service.remove_workspace(self.workspace_id)
            self.graph_repository.delete_graph(self.workspace_id)
            return True, "Successfully removed the workspace"
        except KeyError:
            return False, f"Workspace not found: {self.workspace_id}"
        except Exception as e:
            return False, f"Failed to delete workspace: {str(e)}"


class SelectVisualizerCommand(Command):
    def __init__(self,
                 graph_context: GraphContext,
                 find_visualizer_by_id: Callable[[str], VisualizerPlugin],
                 args: Dict[str, Any]
                 ) -> None:
        self.graph_context = graph_context
        self.find_visualizer_by_id = find_visualizer_by_id
        self.visualizer_id = args.get('visualizer_id')

    def execute(self) -> Tuple[bool, str]:
        if not self.visualizer_id:
            return False, "No visualizer id provided"
        try:
            visualizer = self.find_visualizer_by_id(self.visualizer_id)
        except KeyError:
            return False, f"Unknown visualizer: {self.visualizer_id}"
        self.graph_context.select_visualizer(visualizer)
        return True, f"Selected {visualizer.name()} as visualizer"


class RefreshDataSourceCommand(Command):
    def __init__(self, graph_context: GraphContext) -> None:
        self.graph_context = graph_context

    def execute(self) -> Tuple[bool, str]:
        try:
            self.graph_context.refresh_data_source()
            return True, "Successfully reloaded the data"
        except KeyError:
            return False, "No data source selected"
        except Exception as e:
            return False, f"Failed to refresh data source: {str(e)}"
