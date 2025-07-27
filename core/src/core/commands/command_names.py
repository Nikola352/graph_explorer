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

    # Workspaces
    SELECT_WORKSPACE = "select-workspace"
    CREATE_WORKSPACE = "create-workspace"
    UPDATE_WORKSPACE = "update-workspace"
    DELETE_WORKSPACE = "delete-workspace"

    SELECT_VISUALIZER = "select-visualizer"
    REFRESH_DATA_SOURCE = "refresh-data-source"
