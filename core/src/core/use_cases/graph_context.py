from typing import List

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.models.workspace import Workspace
from core.repositories.graph_repository import query_graph, save_graph
from core.use_cases import workspaces


class GraphContext(object):
    """
    Class that manages graph-related data for one workspace.
    Holds everything needed to generate a graph visualization.
    """

    def __init__(self,
                 workspace: Workspace,
                 data_source_plugins: List[DataSourcePlugin],
                 visualizer_plugins: List[VisualizerPlugin],
                 ):
        # save as dict for fast lookup
        self.data_source_plugins = {
            p.identifier(): p for p in data_source_plugins}
        self.visualizer_plugins = {
            p.identifier(): p for p in visualizer_plugins}

        self._workspace_id = workspace.id

        if workspace.data_source_id and workspace.data_source_id in self.data_source_plugins:
            self._selected_data_source = self.data_source_plugins[workspace.data_source_id]
            self.refresh_data_source()
        else:
            self._selected_data_source = None

        if workspace.visualizer_id and workspace.visualizer_id in self.visualizer_plugins:
            self._selected_visualizer = self.visualizer_plugins[workspace.visualizer_id]
        elif visualizer_plugins:
            # use the first visualizer as default if none is selected
            self._selected_visualizer = visualizer_plugins[0]

    def get_context(self) -> dict:
        graph_html = ""
        if self._selected_data_source is not None and self._selected_visualizer is not None:
            graph = query_graph(self._workspace_id, [])
            graph_html = self._selected_visualizer.display(graph)

        return {
            "selected_data_source": self._selected_data_source.identifier() if self._selected_data_source else None,
            "selected_visualizer": self._selected_visualizer.identifier() if self._selected_visualizer else None,
            "datasources": self.data_source_plugins.values(),
            "visualizers": self.visualizer_plugins.values(),
            "graph_html": graph_html
        }

    def select_data_source(self, data_source_id: str):
        self._selected_data_source = self.data_source_plugins[data_source_id]
        workspaces.set_data_source(self._workspace_id, data_source_id)
        self.refresh_data_source()

    def refresh_data_source(self):
        if self._selected_data_source is None:
            raise KeyError("No data source selected")
        graph = self._selected_data_source.load()
        save_graph(self._workspace_id, graph)

    def select_visualizer(self, visualizer_id: str):
        self._selected_visualizer = self.visualizer_plugins[visualizer_id]
        workspaces.set_visualizer(self._workspace_id, visualizer_id)
