"""
This module provides functions for workspace management.

It uses workspace repository as a persistence layer to provide CRUD operations.
The module handles all workspace-related operations including:
- Workspace creation and deletion
- Workspace retrieval
- Workspace property updates (name, filters, data sources, visualizers)
"""

from typing import List

from core.models.workspace import Workspace
from core.repositories.workspace_repository import WorkspaceRepository


class WorkspaceService(object):
    """
    Provides functions for workspace management.
    """

    def __init__(self, repo: WorkspaceRepository):
        """
        Initializes workspace store and creates a default workspace if no workspaces exist.
        """
        self.repo = repo

        workspaces = self.get_workspaces()
        if not workspaces:
            self.create_workspace("Default Workspace")

    def create_workspace(self, name: str) -> Workspace:
        """
        Creates an empty workspace with the given name.
        
        :param name: The name of the new workspace.
        :type name: str
        :return: Newly created workspace
        :rtype: Workspace
        """
        return self.repo.insert(Workspace("", name))

    def remove_workspace(self, id: str):
        """
        Deletes a workspace with the specified ID.

        :param id: The ID of the workspace to remove
        :type id: str
        :raises KeyError: If no workspace exists with the given ID
        :return: Doesn't return anything but removes the workspace
        :rtype: None
        """
        self.repo.delete(id)

    def get_workspaces(self) -> List[Workspace]:
        """
        Retrieves all available workspaces.

        :return: List of all workspaces
        :rtype: List[Workspace]
        """
        return self.repo.get_all()

    def get_workspace(self, id: str) -> Workspace | None:
        """
        Retrieves a specific workspace by its ID.

        :param id: The ID of the workspace to retrieve
        :type id: str
        :return: The requested workspace or None if not found
        :rtype: Workspace | None
        """
        return self.repo.get(id)

    def set_name(self, workspace_id: str, name: str):
        """
        Updates the name of a workspace.

        :param workspace_id: ID of the workspace to modify
        :type workspace_id: str
        :param name: New name for the workspace
        :type name: str
        :raises KeyError: If no workspace exists with the given ID
        :return: Doesn't return anything but updates the workspace name
        :rtype: None
        """
        workspace = self.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError
        workspace.name = name
        self.repo.update(workspace)

    def set_filters(self, workspace_id: str, filters: List):
        """
        Updates the filters for a workspace.

        :param workspace_id: ID of the workspace to modify
        :type workspace_id: str
        :param filters: New filters to apply to the workspace
        :type filters: Any
        :raises KeyError: If no workspace exists with the given ID
        :return: Doesn't return anything but updates the workspace filters
        :rtype: None
        """
        workspace = self.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError
        workspace.filters = filters
        self.repo.update(workspace)

    def set_data_source(self, workspace_id: str, data_source_id: str):
        """
        Sets the data source for a workspace.

        :param workspace_id: ID of the workspace to modify
        :type workspace_id: str
        :param data_source_id: ID of the data source to associate
        :type data_source_id: str
        :raises KeyError: If no workspace exists with the given ID
        :return: Doesn't return anything but updates the workspace data source
        :rtype: None
        """
        workspace = self.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError
        workspace.data_source_id = data_source_id
        self.repo.update(workspace)

    def set_visualizer(self, workspace_id: str, visualizer_id: str):
        """
        Sets the visualizer for a workspace.

        :param workspace_id: ID of the workspace to modify
        :type workspace_id: str
        :param visualizer_id: ID of the visualizer to associate
        :type visualizer_id: str
        :raises KeyError: If no workspace exists with the given ID
        :return: Doesn't return anything but updates the workspace visualizer
        :rtype: None
        """
        workspace = self.get_workspace(workspace_id)
        if workspace is None:
            raise KeyError
        workspace.visualizer_id = visualizer_id
        self.repo.update(workspace)
