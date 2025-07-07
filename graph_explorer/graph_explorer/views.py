from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render

from core.use_cases.graph_context import GraphContext


def index(request):
    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    return render(request, "index.html", graph_context.get_context())
