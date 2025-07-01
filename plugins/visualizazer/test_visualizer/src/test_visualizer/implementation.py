# TODO: Remove this

from api.components.visualizer import VisualizerPlugin
from api.models.graph import Graph


class TestVisualizer(VisualizerPlugin):
    """
    Visualizer that always returns the same simple graph. Used for testing.
    """

    def name(self) -> str:
        return "Test Visualizer"

    def identifier(self) -> str:
        return "test_visualizer"

    def display(self, graph: Graph, **kwargs) -> str:
        return "<p>graph</p>"
