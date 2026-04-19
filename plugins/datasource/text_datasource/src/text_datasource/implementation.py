from pathlib import Path
from typing import List

from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from api.models.graph import Graph

from .parser import build_graph, tokenize


class TextFileDataSource(DataSourcePlugin):
    """
    A data source that reads graph info from a text file. Matching common competitive programming formats.
    """

    def name(self) -> str:
        return "Text File Data Source"

    def identifier(self) -> str:
        return "text_file_data_source"

    def load(self, **kwargs) -> Graph:
        filename = kwargs["filename"]
        has_labels = kwargs.get("has_labels", False)
        zero_based = kwargs.get("zero_based", False)
        directed = kwargs.get("directed", True)
        weighted = kwargs.get("weighted", False)
        text = Path(filename).read_text()
        tokens = tokenize(text)
        return build_graph(tokens, has_labels, zero_based, directed, weighted)

    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        P = DataSourceConfigParam
        return [
            P("filename", P.Type.STRING, "File Path", required=True),
            P("has_labels", P.Type.BOOLEAN, "Has Node Labels", required=False, default=False),
            P("zero_based", P.Type.BOOLEAN, "Zero-Based Indexes", required=False, default=False),
            P("directed", P.Type.BOOLEAN, "Directed Graph", required=False, default=True),
            P("weighted", P.Type.BOOLEAN, "Weighted Edges", required=False, default=False),
        ]
