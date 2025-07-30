from api.models.node import Node
from api.models.graph import Graph
from api.models.edge import Edge
from api.components.data_source import DataSourcePlugin
from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from typing import List, Type
from .services import create_graph


class SpotifyDataSource(DataSourcePlugin):
    """
    A data source that always returns an empty graph. Used for testing.
    """

    def name(self) -> str:
        return "Spotify Data Source"

    def identifier(self) -> str:
        return "spotify_data_source"

    def load(self, **kwargs) -> Graph:
        auth_token = kwargs["auth_token"]
        artist_name = kwargs["artist_name"]
        max_neighbours = int(kwargs["max_neighbours"])
        recursion_depth = int(kwargs["recursion_depth"])
        return create_graph(auth_token, artist_name, max_neighbours, recursion_depth)

    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        return [
            DataSourceConfigParam(
                name="auth_token", value_type=DataSourceConfigParam.Type.STRING, display_name="Auth Token", required=False),
            DataSourceConfigParam(
                name="artist_name", value_type=DataSourceConfigParam.Type.STRING, display_name="Artist Name"),
            DataSourceConfigParam(
                name="max_neighbours", value_type=DataSourceConfigParam.Type.INT, display_name="Max Neighbours"),
            DataSourceConfigParam(
                name="recursion_depth", value_type=DataSourceConfigParam.Type.INT, display_name="Recursion Depth"),
        ]
