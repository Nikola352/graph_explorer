from abc import ABC, abstractmethod
from typing import List, Optional

from api.models.graph import Graph
from core.models.filter import Filter


class BaseGraphRepository(ABC):
    """
    Interface for graph repository implementations.
    """

    @abstractmethod
    def save_graph(self, id: str, graph: Graph) -> None:
        """
        Save a graph in the database.

        :param id: Unique identifier for the graph
        :param graph: Graph object
        """
        pass

    @abstractmethod
    def query_graph(self, id: str, filters: List[Filter], search_term: str = "") -> Graph:
        """
        Retrieve a graph from the database by ID, applying filters and optional search.

        :param id: Graph ID
        :param filters: List of filters
        :param search_term: Optional search string
        :return: Graph object
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the repository (e.g. database connection).
        """
        pass
