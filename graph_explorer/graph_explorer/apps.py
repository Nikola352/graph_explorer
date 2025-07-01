from django.apps import AppConfig

from core.graph_context import GraphContext
from core.plugin_recognition import PluginService


class GraphExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer'
    plugin_service = PluginService()

    def ready(self):
        self.plugin_service.load_plugins()
        self.graph_context = GraphContext(
            self.plugin_service.data_source_plugins,
            self.plugin_service.visualizer_plugins
        )
