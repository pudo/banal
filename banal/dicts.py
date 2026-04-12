from typing import (
    Any,
    Dict,
    List,
    TypeGuard,
    TypeVar,
    overload,
)
from collections.abc import Mapping

from banal.lists import is_sequence, ensure_list

K = TypeVar("K")
V = TypeVar("V")


def is_mapping(obj: Any) -> TypeGuard[Mapping[Any, Any]]:
    return isinstance(obj, Mapping)


@overload
def ensure_dict(obj: Mapping[K, V]) -> Dict[K, V]:
    pass


@overload
def ensure_dict(obj: Any) -> Dict[Any, Any]:
    pass


def ensure_dict(obj: Any) -> Dict[Any, Any]:
    """Normalize uncertain input into a dict.

    Mappings (and objects with an ``items`` method) are converted via
    dict(obj.items()). Everything else returns an empty dict."""
    # hasattr fallback: legacy compat for dict-likes that aren't Mapping
    if is_mapping(obj) or hasattr(obj, "items"):
        return dict(obj.items())
    return {}


def clean_dict(data: Any) -> Any:
    """Remove None-valued keys from a dictionary, recursively.

    Also filters None values from nested sequences. Non-dict, non-sequence
    values pass through unchanged."""
    if isinstance(data, Mapping):
        out = {}
        for k, v in data.items():
            if v is not None:
                out[k] = clean_dict(v)
        return out
    elif is_sequence(data):
        return [clean_dict(d) for d in data if d is not None]
    return data


def keys_values(data: Dict[K, V], *keys: K) -> List[V]:
    """Look up one or more keys in a dict, returning all found values as a
    flat list. Each value is passed through ensure_list, so scalar values
    are wrapped and None values are dropped."""
    values: List[V] = []
    if isinstance(data, Mapping):
        for key in keys:
            if key in data:
                values.extend(ensure_list(data[key]))
    return values
