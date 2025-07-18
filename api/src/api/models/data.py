from datetime import datetime
from typing import Dict, Union

Value = Union[str, int, float, datetime]
"""
A single value that can be stored under a key in a graph node or edge.

Supported types are string, integer, float and datetime.
"""

DataDict = Dict[str, Value]
"""
Dictionary containing arbitrary data to be saved inside a Node or Edge.

Supported data types are string, integer, float and datetime.
"""
