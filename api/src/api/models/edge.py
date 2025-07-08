from .node import Node


class Edge:
    """
    Class representing an edge in a graph.

    :param src: Source node of the edge.
    :type src: Node
    :param target: Target node of the edge.
    :type target: Node
    :param data: Additional data associated with the edge.
    :type data: dict
    """
    def __init__(self, data: dict, src: Node, target: Node):
        """
        Initializes Edge object.

        :param data: Data stored in an edge.
        :type data: dict
        :param src: Source Node.
        :type src: Node
        :param target: Target Node.
        :type target: Node
        :return: Doesn't return anything but initializes `Edge` object.
        :rtype: None
        """
        self.data = data
        self.src = src
        self.target = target


    def __eq__(self, __value) -> bool:
        """
        Compares this edge to another edge based on their attribute values.

        :param __value: Object to compare with.
        :type __value: Any
        :return: True if the other object is a `Edge` and has the same attribute values, otherwise False.
        :rtype: bool
        """
        if isinstance(__value, Edge):
            return (
                self.data == __value.data and
                self.src == __value.src and 
                self.target == __value.target
            )                

        return False
    
    def __hash__(self) -> int:
        """
        Returns a hash value based on the edge's data.

        :return: Hash of the node.
        :rtype: int
        """
        return hash((self.src, self.target, frozenset(self.data)))
    
    def __str__(self) -> str:
        """
        Returns a string value based on the edge data.

        :return: String representation of edge.
        :rtype: str
        """
        return f"Edge(src_id={self.src.id}, data={self.data}, target_id={self.target.id})"
    
    def __repr__(self) -> str:
        return self.__str__()