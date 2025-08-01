from typing import List

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.models.workspace import Workspace
from core.repositories.graph_repository.implementations.neo4j_graph_repository import Neo4JGraphRepository
from core.use_cases.graph_context import GraphContext
from core.use_cases.workspaces import WorkspaceService


class GraphContextFactory():
    def __init__(self, 
                 workspace_service: WorkspaceService,
                 graph_repository: Neo4JGraphRepository,
                 data_source_plugins: List[DataSourcePlugin],
                 visualizer_plugins: List[VisualizerPlugin]
                 ):
        self.data_source_map = {p.identifier(): p for p in data_source_plugins}
        self.visualizer_map = {p.identifier(): p for p in visualizer_plugins}
        self.workspace_service = workspace_service
        self.graph_repository = graph_repository
        self.visualizer_plugins = visualizer_plugins

    def make(self, workspace: Workspace):
        # Create the initial graph context
        current_data_source = self.data_source_map.get(
            workspace.data_source_id) if workspace.data_source_id else None
        current_visualizer = self.visualizer_map.get(
            workspace.visualizer_id) if workspace.visualizer_id else None
        if current_visualizer is None and self.visualizer_plugins:
            # use the first visualizer as default if none is selected
            current_visualizer = self.visualizer_plugins[0]
        return GraphContext(
            workspace,
            current_data_source,
            current_visualizer,
            self.workspace_service,
            self.graph_repository,
        )
