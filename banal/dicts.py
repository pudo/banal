from collections import Mapping

from banal.lists import is_list


def is_mapping(obj):
    return isinstance(obj, Mapping)


def clean_dict(data):
    """Remove None-valued keys from a dictionary, recursively."""
    if is_mapping(data):
        for k, v in data.items():
            if v is None:
                data.pop(k)
            data[k] = clean_dict(v)
    elif is_list(data):
        return [clean_dict(d) for d in data if d is not None]
    return data
