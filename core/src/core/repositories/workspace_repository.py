from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from tinydb import TinyDB

from core.models.workspace import Workspace


class WorkspaceRepository(object):
    """
    Class responsible for storing and retrieving workspace data using TinyDB.
    """

    def __init__(self, db_filepath: Path):
        """
        Initializes the WorkspaceRepository with the database file path.

        Creates parent directories if they don't exist and initializes the TinyDB connection.

        :param db_filepath: Path to the JSON database file
        :type db_filepath: Path
        """
        db_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(db_filepath)

    def get_all(self) -> List[Workspace]:
        """
        Retrieves all workspaces from the database.

        :return: List of all workspaces in the database
        :rtype: List[Workspace]
        """
        return [Workspace.from_dict({**doc, 'id': str(doc.doc_id)}) for doc in self.db.all()]

    def get(self, id: str) -> Optional[Workspace]:
        """
        Retrieves a single workspace by its ID.

        :param id: The workspace ID to retrieve
        :type id: str
        :return: The requested workspace if found, otherwise None
        :rtype: Optional[Workspace]
        """
        doc = self.db.get(doc_id=int(id))
        if doc is None:
            return None
        doc_dict = cast(Dict[str, Any], doc)
        return Workspace.from_dict({
            **doc_dict,
            "id": str(id),
        })

    def insert(self, workspace: Workspace) -> Workspace:
        """
        Inserts a new workspace into the database.

        :param workspace: The workspace to insert
        :type workspace: Workspace
        :return: The inserted workspace with its new ID set
        :rtype: Workspace
        """
        doc_id = self.db.insert(workspace.to_dict())
        workspace.id = str(doc_id)
        return workspace

    def update(self, workspace: Workspace):
        """
        Updates an existing workspace in the database.

        :param workspace: The workspace to update
        :type workspace: Workspace
        """
        self.db.update(workspace.to_dict(), doc_ids=[int(workspace.id)])

    def delete(self, id: str):
        """
        Deletes a workspace from the database.

        :param id: The ID of the workspace to delete
        :type id: str
        """
        self.db.remove(doc_ids=[int(id)])
