from typing import List

from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from api.models.graph import Graph

from .services import create_graph


class PostgresDataSource(DataSourcePlugin):
    """
    A data source that always returns rows from a PostgreSQL database with relationships between them.
    """

    def name(self) -> str:
        return "PostgreSQL Data Source"

    def identifier(self) -> str:
        return "postgresql_datasource"

    def load(self, **kwargs) -> Graph:
        host = kwargs.get("host")
        port = kwargs.get("port")
        database = kwargs.get("database")
        username = kwargs.get("username")
        password = kwargs.get("password")
        if host is None or port is None or database is None or username is None or password is None:
            return Graph()
        return create_graph(host, int(port), database, username, password)

    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        return [
            DataSourceConfigParam(
                name="host",
                display_name="Host Address",
                value_type=DataSourceConfigParam.Type.STRING,
                default="localhost",
            ),
            DataSourceConfigParam(
                name="port",
                display_name="Port",
                value_type=DataSourceConfigParam.Type.INT,
                default="5432",
            ),
            DataSourceConfigParam(
                name="database",
                display_name="Database name",
                value_type=DataSourceConfigParam.Type.STRING,
            ),
            DataSourceConfigParam(
                name="username",
                display_name="Username",
                value_type=DataSourceConfigParam.Type.STRING,
                default="postgres",
            ),
            DataSourceConfigParam(
                name="password",
                display_name="Password",
                value_type=DataSourceConfigParam.Type.PASSWORD,
            ),
        ]
