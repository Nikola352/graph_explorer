from datetime import datetime

from core.models.filterOperator import FilterOperator


class Filter():
    def __init__(self, field: str, operator: FilterOperator, value: str):
        self.field = field
        self.type = None
        self.operator = operator
        self.parse_value(value)

    def parse_value(self, value) -> object:
        try:
            self.value = int(value)
            self.type = 'int'
            return
        except ValueError:
            pass
        try:
            self.value = float(value)
            self.type = 'float'
            return
        except ValueError:
            pass
        try:
            self.value = datetime.strptime(value, "%Y-%m-%d").date()
            self.type = 'datetime'
            return
        except ValueError:
            pass
        # if string operator can be == or !=
        if self.operator != FilterOperator.EQUALS and self.operator != FilterOperator.NOT_EQUALS:
            raise ValueError("Invalid string operator!")

        self.type = 'str'
        self.value = value

    def __eq__(self, __value) -> bool:
        if isinstance(__value, Filter):
            return (self.field == __value.field
                    and self.operator == __value.operator
                    and self.value == __value.value)
        return False

    def __str__(self) -> str:
        return f"Filter(field: '{self.field}', operator: '{self.operator}', value: '{self.value}', type: '{self.type}')"

    def to_dict(self) -> dict:
        return {
            'field': self.field,
            'operator': self.operator,
            'value': self.value,
            'type': self.type
        }

    @staticmethod
    def from_dict(d: dict) -> "Filter":
        return Filter(
            field=d['field'],
            operator=FilterOperator(d['operator']),
            value=d['value']
        )
