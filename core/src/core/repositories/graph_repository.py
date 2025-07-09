from neo4j import GraphDatabase

from api.models.graph import Graph


class GraphRepository(object):
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def save_graph(self, id: str, graph: Graph):
        pass

    def query_graph(self, id: str, filters: list) -> Graph:
        return Graph()
