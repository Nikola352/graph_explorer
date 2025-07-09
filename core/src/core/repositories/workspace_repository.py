"""
Persistence layer for Workspace objects.

Uses TinyDB to store Workspaces as JSON files in the user data directory.
"""

from typing import Any, Dict, List, cast

from tinydb import TinyDB

from core.constants import DB_FILEPATH
from core.models.workspace import Workspace


def get_db() -> TinyDB:
    DB_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(DB_FILEPATH)


db = get_db()


def get_all() -> List[Workspace]:
    return [Workspace.from_dict({**doc, 'id': str(doc.doc_id)}) for doc in db.all()]


def get(id: str) -> Workspace | None:
    doc = db.get(doc_id=int(id))
    if doc is None:
        return None
    doc_dict = cast(Dict[str, Any], doc)
    return Workspace.from_dict({
        **doc_dict,
        "id": str(id),
    })


def insert(workspace: Workspace) -> Workspace:
    doc_id = db.insert(workspace.to_dict())
    workspace.id = str(doc_id)
    return workspace


def update(workspace: Workspace):
    db.update(workspace.to_dict(), doc_ids=[int(workspace.id)])


def delete(id: str):
    db.remove(doc_ids=[int(id)])
