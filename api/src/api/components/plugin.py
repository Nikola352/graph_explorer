from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    An abstraction representing a platform plugin. All plugin types inherit from this class.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the plugin.

        :return: The name of the plugin.
        :rtype: str
        """
        pass

    @abstractmethod
    def identifier(self) -> str:
        """
        Retrieves a unique identifier for the plugin.

        :return: The unique identifier of the plugin.
        :rtype: str
        """
        pass
