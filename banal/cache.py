import six
from itertools import chain
from hashlib import sha1
from datetime import date, datetime

from banal.dicts import is_mapping
from banal.lists import is_sequence


def bytes_iter(obj):
    """Turn a complex object into an iterator of byte strings.
    The resulting iterator can be used for caching.
    """
    if obj is None:
        yield ''
    elif isinstance(obj, six.binary_type):
        yield obj
    elif isinstance(obj, six.text_type):
        yield obj.encode('utf-8')
    elif is_mapping(obj):
        for key, value in obj.items():
            for out in chain(bytes_iter(key), bytes_iter(value)):
                yield out
    elif is_sequence(obj):
        for item in obj:
            for out in bytes_iter(item):
                yield out
    elif isinstance(obj, (date, datetime)):
        yield obj.isoformat().encode('utf-8')
    else:
        yield unicode(obj).encode('utf-8')


def hash_data(obj):
    """Generate a SHA1 from a complex object."""
    collect = sha1()
    for text in bytes_iter(obj):
        collect.update(text + '$')
    return collect.hexdigest()
