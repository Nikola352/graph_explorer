from abc import abstractmethod

from api.components.plugin import Plugin
from api.models.graph import Graph


class VisualizerPlugin(Plugin):
    """
    An abstraction representing a plugin for visualizing graph data.
    Its task is to output an HTML string for a graph representation based on the given Graph object.

    Plugins must follow integration rules:
    - For interactivity, the following optional attributes can be added:
        * enabled="true" - for elements that should be rendered
        * drag="true" - for nodes that should be draggable
        * tooltip="true" - for elements that should show tooltip on hover
        * zoom="true" - for top-level <svg> or <g> elements that should support zoom/pan
        * click-focus="true" - for elements that should respond to click focus

    - Elements:
        * nodes - tag: <g>, class='node'
        * links - tag: <path>, class='link'

    - All elements must be renderable in a single HTML string.
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
