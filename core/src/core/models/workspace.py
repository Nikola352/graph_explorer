class Workspace(object):
    def __init__(self, id: str, name: str, data_source_id: str | None = None, visualizer_id: str | None = None):
        self.id = id
        self.name = name
        self.data_source_id = data_source_id
        self.visualizer_id = visualizer_id
        self.filters = []
