from typing import List, Any
from collections.abc import Sequence


def is_sequence(obj: Any) -> bool:
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes))


def is_listish(obj):
    """Check if something quacks like a list."""
    if isinstance(obj, (list, tuple, set)):
        return True
    return is_sequence(obj)


def unique_list(lst: Sequence) -> List:
    """Make a list unique, retaining order of initial appearance."""
    uniq = []
    for item in lst:
        if item not in uniq:
            uniq.append(item)
    return uniq


def ensure_list(obj: Any) -> List:
    """Make the returned object a list, otherwise wrap as single item."""
    if obj is None:
        return []
    if not is_listish(obj):
        return [obj]
    return [o for o in obj]


def first(lst: Sequence) -> Any:
    """Return the first non-null element in the list, or None."""
    for item in ensure_list(lst):
        if item is not None:
            return item
