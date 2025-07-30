from abc import ABC, abstractmethod
from typing import Tuple


class Command(ABC):
    """Abstract base class for graph commands following Open/Closed principle."""

    @abstractmethod
    def execute(self) -> Tuple[bool, str]:
        """
        Execute the command.

        :param graph: The graph object to operate on
        :type graph: Graph
        :param args: Dictionary of command arguments
        :type args: Dict[str, Any]

        :return: Tuple of success and message
        :rtype: Tuple[bool, str]
        """
        pass
