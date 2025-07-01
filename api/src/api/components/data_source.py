from abc import abstractmethod
from typing import List

from api.components.plugin import Plugin
from api.models.graph import Graph


class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading graph data from a given data source.
    """

    @abstractmethod
    def load(self, **kwargs) -> Graph:
        """
        Loads graph data from the data source and returns it as a Graph object.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: dict
        :return: A Graph object representing a graph.
        :rtype: Graph
        """
        pass
