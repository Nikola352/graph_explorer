from typing import Any, Dict, Tuple

from core.commands.command import Command
from core.models.filter import Filter
from core.models.filterOperator import FilterOperator
from core.use_cases.graph_context import GraphContext


class SearchCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        query = self.args.get('query')
        if not query:
            return False, 'Query is required.'

        self.graph_context.search_term = query
        return True, f'Search query: {query}'


class FilterCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        field = self.args.get('field')
        operator = self.args.get('operator')
        value = self.args.get('value')

        if not field or not operator or not value:
            return False, 'All filter parameters are required.'

        new_filter = Filter(field=field, operator=FilterOperator(
            operator), value=value)

        if new_filter in self.graph_context.filters:
            return False, "Filter already exists!"

        self.graph_context.add_filter(new_filter)
        return True, f'Filter added: {new_filter}'


class ClearSearchCommand(Command):
    def __init__(self, graph_context: GraphContext) -> None:
        self.graph_context = graph_context

    def execute(self) -> Tuple[bool, str]:
        self.graph_context.search_term = ""
        return True, "Cleared search query"


class RemoveFilterCommand(Command):
    def __init__(self, graph_context: GraphContext, args: Dict[str, Any]) -> None:
        self.graph_context = graph_context
        self.args = args

    def execute(self) -> Tuple[bool, str]:
        field = self.args.get('field')
        operator = self.args.get('operator')
        value = self.args.get('value')

        if not field or not operator or not value:
            return False, "Fields are required!"

        choises = FilterOperator.choices()

        filter = Filter(field, FilterOperator(choises[operator]), value)
        self.graph_context.remove_filter(filter)

        return True, "Filter removed"
