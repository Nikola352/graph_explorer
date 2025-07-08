from typing import List

import core.repositories.workspace_repository as repo
from core.constants import DB_FILEPATH
from core.models.workspace import Workspace


def initialize_workspaces():
    workspaces = get_workspaces()
    if not workspaces:
        create_workspace("Default Workspace")


def create_workspace(name: str) -> Workspace:
    return repo.insert(Workspace("", name))


def remove_workspace(id: str):
    repo.delete(id)


def get_workspaces() -> List[Workspace]:
    return repo.get_all()


def get_workspace(id: str) -> Workspace | None:
    return repo.get(id)


def set_name(workspace_id: str, name: str):
    workspace = get_workspace(workspace_id)
    if workspace is None:
        raise KeyError
    workspace.name = name
    repo.update(workspace)


def set_filters(workspace_id: str, filters):
    workspace = get_workspace(workspace_id)
    if workspace is None:
        raise KeyError
    workspace.filters = filters
    repo.update(workspace)


def set_data_source(workspace_id: str, data_source_id: str):
    workspace = get_workspace(workspace_id)
    if workspace is None:
        raise KeyError
    workspace.data_source_id = data_source_id
    repo.update(workspace)


def set_visualizer(workspace_id: str, visualizer_id: str):
    workspace = get_workspace(workspace_id)
    if workspace is None:
        raise KeyError
    workspace.visualizer_id = visualizer_id
    repo.update(workspace)
