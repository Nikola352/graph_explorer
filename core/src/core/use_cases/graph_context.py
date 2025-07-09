from typing import List

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.models.workspace import Workspace
from core.repositories.graph_repository import query_graph, save_graph
from core.use_cases import workspaces


class GraphContext(object):
    """
    A class that manages graph-related data and visualization for a workspace.

    This class serves as the central point for:
    - Handling graph data loading and visualization
    - Maintaining workspace-specific graph state

    :ivar data_source_plugins: Available data source plugins
    :vartype data_source_plugins: Dict[str, DataSourcePlugin]
    :ivar visualizer_plugins: Available visualizer plugins
    :vartype visualizer_plugins: Dict[str, VisualizerPlugin]
    :ivar _workspace_id: ID of the associated workspace
    :vartype _workspace_id: str
    :ivar _selected_data_source: Currently selected data source
    :vartype _selected_data_source: Optional[DataSourcePlugin]
    :ivar _selected_visualizer: Currently selected visualizer
    :vartype _selected_visualizer: Optional[VisualizerPlugin]
    """

    def __init__(self,
                 workspace: Workspace,
                 data_source_plugins: List[DataSourcePlugin],
                 visualizer_plugins: List[VisualizerPlugin],
                 ):
        """
        Initializes the GraphContext with workspace and plugins.

        :param workspace: The workspace this context belongs to
        :type workspace: Workspace
        :param data_source_plugins: List of available data source plugins
        :type data_source_plugins: List[DataSourcePlugin]
        :param visualizer_plugins: List of available visualizer plugins
        :type visualizer_plugins: List[VisualizerPlugin]
        """
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
        """
        Retrieves the complete graph context state.

        :return: Dictionary containing:
            - selected_data_source: ID of current data source
            - selected_visualizer: ID of current visualizer
            - datasources: Available data sources
            - visualizers: Available visualizers
            - graph_html: Rendered graph HTML
        :rtype: dict
        """
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
        """
        Changes the active data source.

        :param data_source_id: ID of the data source to select
        :type data_source_id: str
        :raises KeyError: If the data source ID is not found
        """
        self._selected_data_source = self.data_source_plugins[data_source_id]
        workspaces.set_data_source(self._workspace_id, data_source_id)
        self.refresh_data_source()

    def refresh_data_source(self):
        """
        Reloads data from the current data source.

        :raises KeyError: If no data source is selected
        """
        if self._selected_data_source is None:
            raise KeyError("No data source selected")
        graph = self._selected_data_source.load()
        save_graph(self._workspace_id, graph)

    def select_visualizer(self, visualizer_id: str):
        """
        Changes the active visualizer.

        :param visualizer_id: ID of the visualizer to select
        :type visualizer_id: str
        :raises KeyError: If the visualizer ID is not found
        """
        self._selected_visualizer = self.visualizer_plugins[visualizer_id]
        workspaces.set_visualizer(self._workspace_id, visualizer_id)
