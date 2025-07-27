import json

from django.apps import apps
from django.http import (HttpRequest, HttpResponse, HttpResponseNotAllowed,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from core.application import Application
from core.commands.command_names import CommandNames
from core.commands.command_processor import CommandProcessor
from core.models.filter import Filter, FilterOperator
from core.use_cases.graph_context import GraphContext
from core.use_cases.workspaces import WorkspaceService


def index(request):
    graph_context: GraphContext = apps.get_app_config(
        'graph_explorer').graph_context  # type: ignore

    core_app: Application = apps.get_app_config(
        'graph_explorer').core_app  # type: ignore

    context = core_app.get_context()
    current_workspace = next(
        (w for w in context["workspaces"] if w.id == context["current_workspace_id"]), None)
    context["filters"] = current_workspace.filters if current_workspace else [""]
    context["search_term"] = graph_context.search_term
    if current_workspace:
        graph = graph_context._graph_repository.query_graph(
            current_workspace.id, [])
        context["graph"] = graph
        context["current_workspace"] = current_workspace
        context["graph_nodes"] = [{"id": n.id, "data": n.data}
                                  for n in graph.get_nodes()]
        context["graph_edges"] = [
            {"src": e.src.id, "tgt": e.target.id, "data": e.data} for e in graph.get_edges()]
    else:
        context["current_workspace"] = None
        context["graph_nodes"] = []
        context["graph_edges"] = []
    return render(request, "index.html", context)


@csrf_protect
def filter_view(request: HttpRequest):
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            attribute = data.get("attribute")
            operator = data.get("operator")
            value = data.get("value")
            if operator == "" or value == "" or attribute == "":
                raise ValueError("Fields are required!")

            success, message = processor.execute_command(CommandNames.FILTER, {
                "field": attribute,
                "operator": operator,
                "value": value,
            })

            if not success:
                return JsonResponse({"error": message}, status=422)

            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def select_visualizer(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    try:
        data = json.loads(request.body)
        visualizer_id = data.get("visualizer_id")
        if visualizer_id is None:
            return JsonResponse({"error": "Missing 'visualizer_id'"}, status=400)

        success, message = processor.execute_command(
            CommandNames.SELECT_VISUALIZER, {"visualizer_id": visualizer_id})

        if not success:
            return JsonResponse({"error": message}, status=400)

        return redirect('index')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"error": f"Visualizer not found: {visualizer_id}"}, status=400)


def select_workspace(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    try:
        data = json.loads(request.body)
        workspace_id = data.get("workspace_id")
        if workspace_id is None:
            return JsonResponse({"error": "Missing 'workspace_id'"}, status=400)

        success, message = processor.execute_command(
            CommandNames.SELECT_WORKSPACE, {"workspace_id": workspace_id})

        if not success:
            return JsonResponse({"error": message}, status=400)

        return JsonResponse({"message": message})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"error": f"Workspace not found: {workspace_id}"}, status=400)


def workspace_form(request: HttpRequest) -> HttpResponse:
    app: Application = apps.get_app_config(
        'graph_explorer').core_app  # type: ignore
    return render(request, "workspace_form.html", app.get_context())


def save_workspace(request: HttpRequest) -> HttpResponse:
    if request.method not in ["POST", "PUT"]:
        return HttpResponseNotAllowed(["POST", "PUT"])

    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    try:
        data = json.loads(request.body)

        if request.method == "POST":
            success, message = processor.execute_command(
                CommandNames.CREATE_WORKSPACE, data)
        else:  # PUT
            success, message = processor.execute_command(
                CommandNames.UPDATE_WORKSPACE, data)

        if not success:
            return JsonResponse({"error": message}, status=400)

        return JsonResponse({"message": message})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def delete_workspace(request: HttpRequest, workspace_id: str) -> HttpResponse:
    if request.method != "DELETE":
        return HttpResponseNotAllowed(['DELETE'])

    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    success, message = processor.execute_command(
        CommandNames.DELETE_WORKSPACE, {"workspace_id": workspace_id})

    if not success:
        return JsonResponse({"error": message}, status=400)

    return JsonResponse({"message": message})


@csrf_protect
def search_view(request: HttpRequest):
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            attribute = data.get("query")
            if attribute == None:
                raise ValueError("Query are required!")

            success, message = processor.execute_command(CommandNames.SEARCH, {
                "query": attribute,
            })

            if not success:
                return JsonResponse({"error": message}, status=400)

            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)


def remove_filter(request: HttpRequest):
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            field = data.get("field")
            operator = data.get("operator")
            value = data.get("value")
            if not field or not operator or not value:
                raise ValueError("Fields are required!")

            success, message = processor.execute_command(CommandNames.REMOVE_FILTER, {
                "field": field,
                "operator": operator,
                "value": value,
            })
            if not success:
                return JsonResponse({"error": message}, status=400)

            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=422)
    return JsonResponse({"error": "Only POST allowed"}, status=405)


def remove_search(request: HttpRequest):
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            search_term = data.get("search_term")
            if not search_term:
                raise ValueError("Fields are required!")
            success, message = processor.execute_command(
                CommandNames.CLEAR_SEARCH, {})
            if not success:
                return JsonResponse({"error": message}, status=400)
            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=422)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def data_source_config(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'])

    data_source_id = request.GET.get('data_source_id')
    if not data_source_id:
        return JsonResponse({"error": "Missing 'data_source_id'"}, status=400)

    app: Application = apps.get_app_config(
        'graph_explorer').core_app  # type: ignore

    params = app.get_data_source_config_params(data_source_id)
    param_dicts = []
    for param in params:
        param_dicts.append(param.to_dict())

    return JsonResponse({"params": param_dicts})


def refresh_data_source(_: HttpRequest) -> HttpResponse:
    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    success, message = processor.execute_command(
        CommandNames.REFRESH_DATA_SOURCE, {})

    if not success:
        return JsonResponse({"error": message}, status=400)

    return JsonResponse({"message": message})


@csrf_exempt
def cli_command_view(request: HttpRequest) -> HttpResponse:
    """
    Handle CLI commands from web interface.
    """

    processor: CommandProcessor = apps.get_app_config(
        'graph_explorer').command_processor  # type: ignore

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command')
            args = data.get('args', {})

            if not command:
                return JsonResponse({
                    'success': False,
                    'message': 'No command specified',
                })

            try:
                success, message = processor.execute_command(command, args)
            except Exception as e:
                success = False
                message = f"Command execution failed: {str(e)}"

            return JsonResponse({
                'success': success,
                'message': message,
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data',
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error processing command: {str(e)}',
            })

    return JsonResponse({
        'success': False,
        'message': 'Only POST method allowed',
    })
