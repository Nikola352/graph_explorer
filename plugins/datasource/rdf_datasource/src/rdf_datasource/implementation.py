from api.models.graph import Graph
from api.components.data_source import DataSourceConfigParam, DataSourcePlugin
from typing import List
from .services import ProxyRdfGraph

class RdfDataSource(DataSourcePlugin):
  
  def __init__(self):
    self.proxy_rdf_graph = ProxyRdfGraph("./plugins/datasource/rdf_datasource/data/graph.ttl")
  
  def name(self) -> str:
    return "RDF Data Source"
    
  def identifier(self) -> str:
    return "rdf_data_source"
    
  def load(self, **kwargs) -> Graph:
    return self.proxy_rdf_graph.create_graph()
    
  def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
    return []
    