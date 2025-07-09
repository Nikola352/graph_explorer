"""
Persistence layer for Workspace objects.

Uses TinyDB to store Workspaces as JSON files in the user data directory.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from tinydb import TinyDB

from core.models.workspace import Workspace


class WorkspaceRepository(object):
    def __init__(self, db_filepath: Path):
        db_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(db_filepath)

    def get_all(self) -> List[Workspace]:
        return [Workspace.from_dict({**doc, 'id': str(doc.doc_id)}) for doc in self.db.all()]

    def get(self, id: str) -> Optional[Workspace]:
        doc = self.db.get(doc_id=int(id))
        if doc is None:
            return None
        doc_dict = cast(Dict[str, Any], doc)
        return Workspace.from_dict({
            **doc_dict,
            "id": str(id),
        })

    def insert(self, workspace: Workspace) -> Workspace:
        doc_id = self.db.insert(workspace.to_dict())
        workspace.id = str(doc_id)
        return workspace

    def update(self, workspace: Workspace):
        self.db.update(workspace.to_dict(), doc_ids=[int(workspace.id)])

    def delete(self, id: str):
        self.db.remove(doc_ids=[int(id)])
