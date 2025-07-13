# TODO: Remove this

from typing import List

from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node


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

    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        return []
