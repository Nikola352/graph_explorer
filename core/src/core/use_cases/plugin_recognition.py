from importlib.metadata import entry_points
from typing import List, Tuple

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.config.constants import (DATA_SOURCE_PLUGIN_GROUP_NAME,
                                   VISUALIZER_PLUGIN_GROUP_NAME)


def load_plugins() -> Tuple[List[DataSourcePlugin], List[VisualizerPlugin]]:
    return load_data_source_plugins(), load_visualizer_plugins()


def load_data_source_plugins() -> List[DataSourcePlugin]:
    plugins = []
    for entry_point in entry_points(group=DATA_SOURCE_PLUGIN_GROUP_NAME):
        p = entry_point.load()
        plugin: DataSourcePlugin = p()
        plugins.append(plugin)
    return plugins


def load_visualizer_plugins() -> List[VisualizerPlugin]:
    plugins = []
    for entry_point in entry_points(group=VISUALIZER_PLUGIN_GROUP_NAME):
        p = entry_point.load()
        plugin: VisualizerPlugin = p()
        plugins.append(plugin)
    return plugins
