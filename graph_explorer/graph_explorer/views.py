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

    print([w.to_dict() for w in workspaces.get_workspaces()])

    return render(request, "index.html", core_app.get_context())
