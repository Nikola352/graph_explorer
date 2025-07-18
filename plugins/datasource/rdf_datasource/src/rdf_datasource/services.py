
from api.models.edge import Edge
from api.models.graph import Graph
from api.models.node import Node
from rdflib import Graph as RdfGraph
from abc import abstractmethod
from rdflib.namespace import Namespace

EX = Namespace("http://example.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

class RdfGraphAbstract(): # Abstract interface
  @abstractmethod
  def load(self):
    pass
  
class RealRdfGraph(RdfGraphAbstract): # Concrete implementation 
  def __init__(self, filename: str):
    self.filename = filename
    self.graph = RdfGraph()
    
  def load(self) -> RdfGraph:
    self.graph.parse(self.filename, format='turtle')
    return self.graph
  
class ProxyRdfGraph(RdfGraphAbstract): # Proxy
  def __init__(self, filename: str):
    self.filename = filename
    self.rdf_graph = None
    self.graph = None
    
  def load(self) -> RdfGraph:
    if self.rdf_graph is None:
      self.rdf_graph = RealRdfGraph(self.filename).load()
    return self.rdf_graph
    
  def create_graph(self) -> Graph:
    self.load()
    graph = Graph(directed=True, root_id=None)
    node_map = {}
    
    for s, _, o in self.rdf_graph.triples((None, EX.knows, None)):
      if s not in node_map:
        age = None
        gender = None
        for s, _, obj in self.rdf_graph.triples((s, EX.age, None)):
          age = int(obj) if obj else None
        for s, _, obj in self.rdf_graph.triples((s, EX.gender, None)):
          gender = obj
        data = {
          "name": s.split("/")[-1],
          "age": age,
          "gender": gender
        }
        node = Node(s, data)
        graph.add_node(node)
        node_map[s] = node
        
      if o not in node_map:
        age = None
        gender = None
        for s, _, obj in self.rdf_graph.triples((o, EX.age, None)):
          age = int(obj) if obj else None
        for s, _, obj in self.rdf_graph.triples((o, EX.gender, None)):
          gender = obj
        data = {
          "name": o.split("/")[-1],
          "age": age,
          "gender": gender
        }
        node = Node(o, data)
        graph.add_node(node)
        node_map[o] = node
        
      if (s, o) not in graph.edges:
        graph.add_edge(Edge({"connection": "knows"}, node_map[s], node_map[o]))
    return graph
  
  

 
