from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from api.components.plugin import Plugin
from api.models.graph import Graph


class DataSourceConfigParam(object):
    """
    A class representing a configuration parameter for a data source.

    :var name: The unique identifier name of the parameter.
    :vartype name: str
    :var value_type: The data type of the parameter value.
    :vartype value_type: DataSourceConfigParam.Type
    :var display_name: The human-readable name for display purposes. 
                         Defaults to the parameter name if not provided.
    :vartype display_name: Optional[str]
    :var required: Whether the parameter is required. Defaults to True.
    :vartype required: bool
    :var options: For CHOICE type parameters, the list of available options.
                    Can be a list of values or a list of {value, display} dicts.
    :vartype options: Optional[Union[List[str], List[Dict[str, str]]]]
    :var default: The default value for the parameter.
    :vartype default: Optional[Any]
    """

    class Type(str, Enum):
        """
        Enumeration of supported parameter types for data source configuration.

        :cvar STRING: String type parameter
        :cvar INT: Integer type parameter
        :cvar FLOAT: Floating-point number type parameter
        :cvar BOOLEAN: Boolean type parameter
        :cvar DATE: Date type parameter
        :cvar DATETIME: Datetime type parameter
        :cvar URL: URL type parameter
        :cvar EMAIL: Email address type parameter
        :cvar CHOICE: Choice from predefined options type parameter
        :cvar PASSWORD: Sensitive credential type parameter
        """
        STRING = "str"
        INT = "int"
        FLOAT = "float"
        BOOLEAN = "bool"
        DATE = "date"
        DATETIME = "datetime"
        URL = "url"
        EMAIL = "email"
        CHOICE = "choice"
        PASSWORD = "password"

    def __init__(self,
                 name: str,
                 value_type: Type,
                 display_name: Optional[str] = None,
                 required: bool = True,
                 options: Optional[Union[List[str],
                                         List[Dict[str, str]]]] = None,
                 default: Optional[Union[str, int, float, bool]] = None):
        """
        Initialize a configuration parameter.

        :param name: The unique identifier name of the parameter.
        :type name: str
        :param value_type: The data type of the parameter value.
        :type value_type: DataSourceConfigParam.Type
        :param display_name: The human-readable name for display purposes. 
                            Defaults to the parameter name if not provided.
        :type display_name: Optional[str]
        :param required: Whether the parameter is required. Defaults to True.
        :type required: bool
        :param options: For CHOICE type parameters, the list of available options.
                        Can be a list of values or a list of {value, display} dicts.
        :type options: Optional[Union[List[str], List[Dict[str, str]]]]
        :param default: The default value for the parameter.
        :type default: Optional[Any]

        :raises ValueError: If options are provided for non-CHOICE type or
                           if required CHOICE type has no options.
        """
        self.name = name
        self.value_type = value_type
        self.display_name = display_name if display_name is not None else name
        self.required = required
        self.default = default

        if value_type == self.Type.CHOICE:
            if not options:
                raise ValueError("CHOICE type parameter must have options")
            self.options = self._normalize_options(options)
        elif options is not None:
            raise ValueError(
                "Options can only be specified for CHOICE type parameters")

    def _normalize_options(self, options: Union[List[str], List[Dict[str, str]]]) -> List[Dict[str, str]]:
        """
        Normalize options to a consistent format of {value: display}.

        :param options: The options to normalize
        :type options: Union[List[str], List[Dict[str, str]]]
        :return: Normalized options in {value: display} format
        :rtype: List[Dict[str, str]]
        """
        normalized = []
        for option in options:
            if isinstance(option, dict):
                if "value" not in option or "display" not in option:
                    raise ValueError(
                        "Option dictionaries must contain 'value' and 'display' keys")
                normalized.append(
                    {"value": str(option["value"]), "display": option["display"]})
            else:
                normalized.append(
                    {"value": str(option), "display": str(option)})
        return normalized

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns the dictionary representation of the configuration parameter.
        Suitable for serialization.
        """
        d = {
            'name': self.name,
            'value_type': self.value_type,
            'display_name': self.display_name,
            'required': self.required,
            'default': self.default,
        }
        if hasattr(self, 'options'):
            d['options'] = self.options
        return d


class DataSourcePlugin(Plugin):
    """
    An abstraction representing a plugin for loading graph data from a given data source.
    """

    @abstractmethod
    def load(self, **kwargs) -> Graph:
        """
        Loads graph data from the data source and returns it as a Graph object.

        :param kwargs: Arbitrary keyword arguments for customization or filtering of the data loading process.
        :type kwargs: dict
        :return: A Graph object representing a graph.
        :rtype: Graph
        """
        pass

    @abstractmethod
    def get_configuration_parameters(self) -> List[DataSourceConfigParam]:
        """
        Retrieves the list of configuration parameters required by this data source.

        :return: A list of DataSourceConfigParam objects describing the required parameters.
        :rtype: List[DataSourceConfigParam]
        """
        pass
