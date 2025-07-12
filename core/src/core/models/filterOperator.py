from enum import Enum


class FilterOperator(str, Enum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    # CONTAINS = "contains"
    # STARTS_WITH = "startswith"
    # ENDS_WITH = "endswith"

    def symbol(self) -> str:
        return {
            FilterOperator.EQUALS: "==",
            FilterOperator.NOT_EQUALS: "!=",
            FilterOperator.GREATER_THAN: ">",
            FilterOperator.LESS_THAN: "<",
            FilterOperator.LESS_THAN_OR_EQUAL: "<=",
            FilterOperator.GREATER_THAN_OR_EQUAL: ">="
            # FilterOperator.CONTAINS: "CONTAINS",
            # FilterOperator.STARTS_WITH: "STARTS WITH",
            # FilterOperator.ENDS_WITH: "ENDS WITH"
        }[self]

    def __str__(self) -> str:
        return self.symbol()

    @classmethod
    def choices(cls) -> dict:
        return {op.symbol(): op.value for op in cls}
