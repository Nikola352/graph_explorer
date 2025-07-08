class Workspace(object):
    def __init__(self,
                 id: str,
                 name: str,
                 data_source_id: str | None = None,
                 visualizer_id: str | None = None,
                 filters: list = [],
                 ):
        self.id = id
        self.name = name
        self.data_source_id = data_source_id
        self.visualizer_id = visualizer_id
        self.filters = filters

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "data_source_id": self.data_source_id,
            "visualizer_id": self.visualizer_id,
            "filters": self.filters,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Workspace':
        workspace = cls(
            id=data['id'],
            name=data['name'],
            data_source_id=data.get('data_source_id'),
            visualizer_id=data.get('visualizer_id'),
            filters=data.get('filters', [])
        )
        return workspace
