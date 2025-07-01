from typing import List

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin


class GraphContext(object):
    def __init__(self, data_source_plugins: List[DataSourcePlugin], visualizer_plugins: List[VisualizerPlugin]) -> None:
        # select first data source and visualizer from the list as default
        self._selected_data_source = data_source_plugins[0] if data_source_plugins else None
        self._selected_visualizer = visualizer_plugins[0] if visualizer_plugins else None

        # save as dict for fast lookup
        self.data_source_plugins = {
            p.identifier(): p for p in data_source_plugins}
        self.visualizer_plugins = {
            p.identifier(): p for p in visualizer_plugins}

    def get_context(self) -> dict:
        if not self._selected_data_source or not self._selected_visualizer:
            return {}
        # TODO: Use persistance layer instead of loading from the data source every time
        graph = self._selected_data_source.load()
        graph_html = self._selected_visualizer.display(graph)
        return {"graph_html": graph_html}

    def select_datasource(self, data_source_id: str) -> None:
        self._selected_data_source = self.data_source_plugins[data_source_id]

    def select_visualizer(self, visualizer_id: str) -> None:
        self._selected_visualizer = self.visualizer_plugins[visualizer_id]
