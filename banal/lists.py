import six
from collections import Sequence


def is_sequence(obj):
    """Check if something quacks like a list."""
    return isinstance(obj, Sequence) and not isinstance(obj, six.string_types)


def unique_list(lst):
    """Make a list unique, retaining order of initial appearance."""
    uniq = []
    for item in lst:
        if item not in uniq:
            uniq.append(item)
    return uniq


def ensure_list(obj):
    """Make the returned object a list, otherwise wrap as single item."""
    if obj is None:
        return []
    if not is_sequence(obj):
        return [obj]
    return obj


