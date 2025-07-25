from abc import ABC, abstractmethod
from typing import List, Optional

from core.models.workspace import Workspace


class BaseWorkspaceRepository(ABC):
    """
    Interface for workspace repository implementations.
    """

    @abstractmethod
    def get_all(self) -> List[Workspace]:
        """
        Retrieve all workspaces.

        :return: List of all workspaces in the database
        :rtype: List[Workspace]
        """
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Workspace]:
        """
        Retrieve a workspace by its ID.

        :param id: The workspace ID to retrieve
        :type id: str
        :return: The requested workspace if found, otherwise None
        :rtype: Optional[Workspace]
        """
        pass

    @abstractmethod
    def insert(self, workspace: Workspace) -> Workspace:
        """
        Insert a new workspace.

        :param workspace: The workspace to insert
        :type workspace: Workspace
        :return: The inserted workspace with its new ID set
        :rtype: Workspace
        """
        pass

    @abstractmethod
    def update(self, workspace: Workspace) -> Workspace:
        """
        Update an existing workspace.

        :param workspace: The workspace to update
        :type workspace: Workspace
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Delete a workspace by ID.

        :param id: The ID of the workspace to delete
        :type id: str
        """
        pass
