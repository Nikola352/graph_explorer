from typing import Dict, List, Optional

from api.models.data import DataDict


class Node:
    """
    Class representing `Node` in a graph.

    Attributes:
        id: str - Node unique identifier 
        data: DataDict - Additional data of a node
        edges: list[Edge] - List of adjecent edges
    """

    def __init__(self, id: str, data: DataDict, edges: Optional[List] = None):
        """
        Initializes node object.

        :param id: Node unique identifier.
        :type id: str
        :param data: Data stored in a node.
        :type data: DataDict
        :param edges: List of adjecent edges of a node.
        :type edges: list["Edge"]
        :return: Doesn't return anything but initializes `Node` object.
        :rtype: None
        """
        self.id = id
        self.data = data
        self.edges = edges if edges else []

    def __eq__(self, __value) -> bool:
        """
        Compares this node to another node based on their ID.

        :param __value: Object to compare with.
        :type __value: Any
        :return: True if the other object is a Node and has the same ID, otherwise False.
        :rtype: bool
        """
        if isinstance(__value, Node):
            return self.id == __value.id
        return False

    def get_neighbours(self) -> List["Node"]:
        """
        Returns a list of neighboring nodes connected by outgoing edges.

        :return: List of adjacent nodes.
        :rtype: list[Node]
        """
        neighbours = []
        for edge in self.edges:
            if edge.src == self:
                neighbours.append(edge.target)
        return neighbours

    def __hash__(self) -> int:
        """
        Returns a hash value based on the node's unique identifier.

        :return: Hash of the node.
        :rtype: int
        """
        return hash(self.id)

    def __str__(self) -> str:
        """
        Returns a string value based on the node data.

        :return: String representation of node.
        :rtype: str
        """
        return f"Node(id={self.id}, data={self.data}, edges={self.edges})"

    def __repr__(self) -> str:
        return self.__str__()
