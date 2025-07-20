from api.models.graph import Graph
from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from typing import List
from .services import ProxyRdfGraph

class RdfDataSource(DataSourcePlugin):
  
  def __init__(self):
    self.proxy_rdf_graph = ProxyRdfGraph()
  
  def name(self) -> str:
    return "RDF Data Source"
    
  def identifier(self) -> str:
    return "rdf_data_source"
    
  def load(self, **kwargs) -> Graph:
    filename = kwargs.get("filename")
    return self.proxy_rdf_graph.create_graph(filename)
    
  def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
    return [
      DataSourceConfigParam(
        name="filename",
        value_type=DataSourceConfigParam.Type.STRING,
        display_name="File Name",
        required=True
      )
    ]
    