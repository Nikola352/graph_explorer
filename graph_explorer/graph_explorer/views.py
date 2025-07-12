import json
from django.apps import apps
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from core.application import Application
from core.models.filter import Filter, FilterOperator
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
    # context["operators"] = ["==", "!=", "<", "<=", ">", ">="]
    return render(request, "index.html", context)


@csrf_protect
def filter_view(request: HttpRequest):
    # try create filter object
    # if error return error else created object send to filter graph
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
            print(new_filter)
            return JsonResponse({"message": "moja poruka", "received": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=422)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
