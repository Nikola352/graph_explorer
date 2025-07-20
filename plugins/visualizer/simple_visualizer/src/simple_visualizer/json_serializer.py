import json
from datetime import datetime


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_json(obj):
    return json.dumps(obj, default=datetime_serializer)
