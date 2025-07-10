from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render

from core.application import Application
from core.use_cases import workspaces
from core.use_cases.graph_context import GraphContext


def index(request):
    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    core_app: Application = apps.get_app_config(
        'graph_explorer').core_app  # type: ignore

    context = core_app.get_context()
    current_workspace = next(
        (w for w in context["workspaces"] if w.id == context["current_workspace_id"]), None)
    context["filters"] = current_workspace.filters if current_workspace else [""]
    context["operators"] = ["==", "!=", "<", "<=", ">", ">="]
    return render(request, "index.html", context)
