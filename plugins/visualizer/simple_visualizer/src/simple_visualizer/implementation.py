import os

from jinja2 import Environment, FileSystemLoader
from simple_visualizer.json_serializer import serialize_json

from api.components.visualizer import VisualizerPlugin
from api.models.graph import Graph


class SimpleVisualizer(VisualizerPlugin):
    """
    A simple plugin-based graph visualizer that uses a Jinja2 HTML template.

    This visualizer renders a graph by injecting its data (nodes, edges, etc.)
    into a pre-defined HTML template.
    """

    def __init__(self) -> None:
        template_path = os.path.join(os.path.dirname(__file__))
        environment = Environment(
            loader=FileSystemLoader(template_path + "/templates"))
        environment.filters['tojson'] = serialize_json
        self.template = environment.get_template(
            "simple_visualizer_template.html")

    def name(self) -> str:
        """
        Returns the display name of the visualizer.

        :return: A human-readable name of the visualizer.
        :rtype: str
        """
        return "Simple visualizer"

    def identifier(self) -> str:
        """
        Returns a unique string identifier for the visualizer.

        :return: A unique identifier used to distinguish this visualizer.
        :rtype: str
        """
        return "simple_visualizer"

    def display(self, graph: Graph, **kwargs) -> str:
        """
        Renders the graph into an HTML string using the template.

        :param graph: The graph to be visualized.
        :type graph: Graph
        :param kwargs: Additional optional keyword arguments for customization.
        :return: The rendered HTML string with graph visualization.
        :rtype: str
        """
        return self.template.render(nodes=graph.get_nodes(), edges=graph.get_edges(), directed=graph.directed, name=self.identifier())
