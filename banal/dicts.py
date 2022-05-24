from typing import (
    Any,
    Dict,
    List,
    Tuple,
    TypeVar,
    Union,
    Mapping as TMapping,
    Iterable,
    Iterator,
)
from collections.abc import Mapping

from banal.lists import is_sequence, ensure_list

K = TypeVar("K")
V = TypeVar("V")


def is_mapping(obj: Any) -> bool:
    return isinstance(obj, Mapping)


def ensure_dict(obj: Any) -> Dict[K, V]:
    if is_mapping(obj) or hasattr(obj, "items"):
        return dict(obj.items())
    return {}


def clean_dict(data: Any) -> Any:
    """Remove None-valued keys from a dictionary, recursively."""
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
    """Get an entry as a list from a dict. Provide a fallback key."""
    values: List[V] = []
    if isinstance(data, Mapping):
        for key in keys:
            if key in data:
                values.extend(ensure_list(data[key]))
    return values


def items(data: Union[TMapping, Iterable]) -> Iterator[Tuple[Any, Any]]:
    if is_mapping(data):
        return data.items()
    else:
        return enumerate(data)
