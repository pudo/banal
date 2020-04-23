from typing import Any, Dict, List
from collections.abc import Mapping

from banal.lists import is_sequence, ensure_list


def is_mapping(obj: Any) -> bool:
    return isinstance(obj, Mapping)


def ensure_dict(obj: Any) -> Dict:
    if is_mapping(obj) or hasattr(obj, 'items'):
        return dict(obj.items())
    return {}


def clean_dict(data: Mapping) -> Mapping:
    """Remove None-valued keys from a dictionary, recursively."""
    if is_mapping(data):
        out = {}
        for k, v in data.items():
            if v is not None:
                out[k] = clean_dict(v)
        return out
    elif is_sequence(data):
        return [clean_dict(d) for d in data if d is not None]  # type: ignore
    return data


def keys_values(data: Dict, *keys: str) -> List:
    """Get an entry as a list from a dict. Provide a fallback key."""
    values = []
    if is_mapping(data):
        for key in keys:
            if key in data:
                values.extend(ensure_list(data[key]))
    return values
