from abc import abstractmethod

from api.components.plugin import Plugin
from api.models.graph import Graph


class VisualizerPlugin(Plugin):
    """
    An abstraction representing a plugin for visualizing graph data. 
    Its task is to output HTML string for a graph representation based on the given Graph object.
    """

    @abstractmethod
    def display(self, graph: Graph, **kwargs) -> str:
        """
        Converts the graph into an HTML string representation.

        :param graph: A Graph object representing a graph to be visualized.
        :type graph: Graph
        :return: An HTML string representation of the given graph.
        :rtype: str
        """
        pass
