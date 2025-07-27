from enum import Enum


class CommandNames(str, Enum):
    # Graph modification
    CREATE_NODE = "create-node"
    UPDATE_NODE = "update-node"
    DELETE_NODE = "delete-node"
    CREATE_EDGE = "create-edge"
    UPDATE_EDGE = "update-edge"
    DELETE_EDGE = "delete-edge"
    CLEAR_GRAPH = "clear-graph"

    # Node filtering
    SEARCH = "search"
    FILTER = "filter"
    CLEAR_SEARCH = "clear-search"
    REMOVE_FILTER = "remove-filter"
