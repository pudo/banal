from hashlib import sha1
from itertools import chain
from typing import Any, Iterable
from datetime import date, datetime

from banal.dicts import is_mapping
from banal.lists import is_sequence

HASH_ENCODING = "utf-8"


def bytes_iter(obj: Any) -> Iterable[bytes]:
    """Recursively decompose an object into an iterator of byte strings.

    Handles None (yields nothing), str, bytes, date/datetime, mappings
    (sorted by key), sequences (sorted when possible), callables (by __name__),
    and falls back to str() for everything else."""
    if obj is None:
        return
    elif isinstance(obj, bytes):
        yield obj
    elif isinstance(obj, str):
        yield obj.encode(HASH_ENCODING)
    elif isinstance(obj, (date, datetime)):
        yield obj.isoformat().encode(HASH_ENCODING)
    elif is_mapping(obj):
        if None in obj:
            yield from bytes_iter(obj[None])
        for key in sorted(k for k in obj.keys() if k is not None):
            for out in chain(bytes_iter(key), bytes_iter(obj[key])):
                yield out
    elif is_sequence(obj):
        if isinstance(obj, (list, set)):
            try:
                obj = sorted(obj)
            except Exception:
                pass
        for item in obj:
            for out in bytes_iter(item):
                yield out
    elif hasattr(obj, "__name__"):
        yield obj.__name__.encode(HASH_ENCODING)
    else:
        yield str(obj).encode(HASH_ENCODING)


def hash_data(obj: Any) -> str:
    """Generate a deterministic SHA1 hex digest from a complex object.

    Key order in mappings and element order in sortable sequences are
    normalized, so structurally equivalent objects produce the same hash."""
    collect = sha1()
    for data in bytes_iter(obj):
        collect.update(data)
    return collect.hexdigest()
