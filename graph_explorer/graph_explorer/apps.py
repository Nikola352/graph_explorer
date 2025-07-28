from django.apps import AppConfig

from core.application import Application
from core.commands.command_processor import CommandProcessor
from core.use_cases.graph_context import GraphContext
from core.use_cases.workspaces import WorkspaceService


class GraphExplorerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer'

    def ready(self):
        self.core_app = Application()

    @property
    def graph_context(self) -> GraphContext:
        return self.core_app.graph_context

    @property
    def workspace_service(self) -> WorkspaceService:
        return self.core_app.workspace_service

    @property
    def command_processor(self) -> CommandProcessor:
        return self.core_app.command_processor
