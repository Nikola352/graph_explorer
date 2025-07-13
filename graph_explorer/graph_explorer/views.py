import json

from django.apps import apps
from django.http import (HttpRequest, HttpResponse, HttpResponseNotAllowed,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from core.application import Application
from core.models.filter import Filter, FilterOperator
from core.use_cases import workspaces
from core.use_cases.graph_context import GraphContext
from core.use_cases.workspaces import WorkspaceService


def index(request):
    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    workspaces: WorkspaceService = apps.get_app_config(
        'graph_explorer').workspace_service  # type: ignore

    core_app: Application = apps.get_app_config(
        'graph_explorer').core_app  # type: ignore

    context = core_app.get_context()
    current_workspace = next(
        (w for w in context["workspaces"] if w.id == context["current_workspace_id"]), None)
    context["filters"] = current_workspace.filters if current_workspace else [""]
    return render(request, "index.html", context)


@csrf_protect
def filter_view(request: HttpRequest):
    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            attribute = data.get("attribute")
            operator = data.get("operator")
            value = data.get("value")
            if operator == "" or value == "" or attribute == "":
                raise ValueError("Fields are required!")
            new_filter = Filter(
                attribute, operator=FilterOperator(operator), value=value)
            graph_context.add_filter(new_filter)
            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=422)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def select_visualizer(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    try:
        data = json.loads(request.body)
        visualizer_id = data.get("visualizer_id")
        if visualizer_id is None:
            return JsonResponse({"error": "Missing 'visualizer_id'"}, status=400)

        graph_context.select_visualizer(visualizer_id)

        return redirect('index')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"error": f"Visualizer not found: {visualizer_id}"}, status=400)
