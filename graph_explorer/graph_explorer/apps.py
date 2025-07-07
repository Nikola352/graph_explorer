from django.apps import AppConfig

from core.application import Application
from core.use_cases.graph_context import GraphContext


class GraphExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer'

    def ready(self):
        self.core_app = Application()

    @property
    def graph_context(self) -> GraphContext:
        return self.core_app.graph_context
