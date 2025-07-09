from pathlib import Path

import appdirs

DATA_SOURCE_PLUGIN_GROUP_NAME = "graph_explorer.datasources"
VISUALIZER_PLUGIN_GROUP_NAME = "graph_explorer.visualizers"

DB_FILEPATH = Path(appdirs.user_data_dir("graph_explorer")) / "workspaces.json"
