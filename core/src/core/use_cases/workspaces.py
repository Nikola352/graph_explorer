import uuid
from typing import List

from core.models.workspace import Workspace


def initialize_workspaces():
    workspaces = get_workspaces()
    if not workspaces:
        create_workspace("Default Workspace")


def create_workspace(name: str) -> Workspace:
    workspace = Workspace(str(uuid.uuid4()), name)
    # TODO: save to db
    return workspace


def remove_workspace():
    pass


def get_workspaces() -> List[Workspace]:
    return [Workspace(str(uuid.uuid4()), "Default workspace", data_source_id="empty_data_source")]


def get_workspace(workspace_id) -> Workspace | None:
    return Workspace(workspace_id, "Default")
