# TODO: Remove this

from api.components.data_source import DataSourcePlugin
from api.models.graph import Graph


class EmptyDataSource(DataSourcePlugin):
    """
    A data source that always returns an empty graph. Used for testing.
    """

    def name(self) -> str:
        return "Empty Data Source"

    def identifier(self) -> str:
        return "empty_data_source"

    def load(self, **kwargs) -> Graph:
        return Graph()
