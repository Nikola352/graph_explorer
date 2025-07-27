from typing import Any, Callable, Dict, Tuple

from core.commands.command import Command
from core.models.workspace import Workspace
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
    def __init__(self, workspace_service: WorkspaceService, select_workspace: Callable[[str], Workspace], args: Dict[str, Any]) -> None:
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
            self.select_workspace(workspace.id)
            return True, f"Created {workspace.name}"
        except Exception as e:
            return False, f"Failed to create workspace: {str(e)}"


class UpdateWorkspaceCommand(Command):
    def __init__(self, workspace_service: WorkspaceService, graph_context: GraphContext, get_current_workspace_id: Callable[[], str], args: Dict[str, Any]):
        self.workspace_service = workspace_service
        self.graph_context = graph_context
        self.get_current_workspace_id = get_current_workspace_id
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

            # Update current workspace context if it's the active one
            if self.get_current_workspace_id() == workspace.id:
                self.graph_context.set_data_source_config(self.config)
                self.graph_context.select_data_source(self.data_source_id)

            return True, f"Updated {workspace.name}"
        except KeyError:
            return False, f"Workspace not found: {self.workspace_id}"
        except Exception as e:
            return False, f"Failed to update workspace: {str(e)}"


class DeleteWorkspaceCommand(Command):
    def __init__(self, workspace_service: WorkspaceService, args: Dict[str, Any]) -> None:
        self.workspace_service = workspace_service
        self.workspace_id = args.get("workspace_id")

    def execute(self) -> Tuple[bool, str]:
        if not self.workspace_id:
            return False, "Missing 'workspace_id'"

        try:
            self.workspace_service.remove_workspace(self.workspace_id)
            return True, "Successfully removed the workspace"
        except KeyError:
            return False, f"Workspace not found: {self.workspace_id}"
        except Exception as e:
            return False, f"Failed to delete workspace: {str(e)}"


class SelectVisualizerCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.visualizer_id = args.get('visualizer_id')

    def execute(self) -> Tuple[bool, str]:
        if not self.visualizer_id:
            return False, "No visualizer id provided"
        visualizer = self.graph_context.select_visualizer(self.visualizer_id)
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
