from typing import List

from core.models.filter import Filter


class Workspace(object):
    """
    A data class representing a workspace. Can be serialized and stored in a persistence layer.
    """

    def __init__(self,
                 id: str,
                 name: str,
                 data_source_id: str | None = None,
                 visualizer_id: str | None = None,
                 filters: List[Filter] = [],
                 data_source_config: dict = {},
                 ):
        self.id = id
        self.name = name
        self.data_source_id = data_source_id
        self.visualizer_id = visualizer_id
        self.filters = filters
        self.data_source_config = data_source_config

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "data_source_id": self.data_source_id,
            "visualizer_id": self.visualizer_id,
            "filters": [f.to_dict() for f in self.filters],
            "data_source_config": self.data_source_config,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Workspace':
        workspace = cls(
            id=data['id'],
            name=data['name'],
            data_source_id=data.get('data_source_id'),
            visualizer_id=data.get('visualizer_id'),
            filters=[Filter.from_dict(f) for f in data.get('filters', [])],
            data_source_config=data.get('data_source_config', {})
        )
        return workspace
