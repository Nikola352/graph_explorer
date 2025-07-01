from importlib.metadata import entry_points
from typing import List

from api.components.data_source import DataSourcePlugin
from api.components.visualizer import VisualizerPlugin
from core.constants import (DATA_SOURCE_PLUGIN_GROUP_NAME,
                            VISUALIZER_PLUGIN_GROUP_NAME)


class PluginService(object):
    def __init__(self) -> None:
        self.data_source_plugins: List[DataSourcePlugin] = []
        self.visualizer_plugins: List[VisualizerPlugin] = []

    def load_plugins(self):
        self.load_data_source_plugins()
        self.load_visualizer_plugins()

    def load_data_source_plugins(self):
        for entry_point in entry_points(group=DATA_SOURCE_PLUGIN_GROUP_NAME):
            p = entry_point.load()
            plugin: DataSourcePlugin = p()
            self.data_source_plugins.append(plugin)

    def load_visualizer_plugins(self):
        for entry_point in entry_points(group=VISUALIZER_PLUGIN_GROUP_NAME):
            p = entry_point.load()
            plugin: VisualizerPlugin = p()
            self.visualizer_plugins.append(plugin)
