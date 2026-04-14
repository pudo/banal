from typing import overload, Optional, Union, List, Set, FrozenSet, Tuple, Any
from typing import TypeVar, Generator, Sequence, Iterable, TypeGuard
from typing_extensions import Never
from collections.abc import MappingView

T = TypeVar("T")


def is_sequence(obj: Any) -> bool:
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes))


def is_listish(
    obj: Any,
) -> TypeGuard[Union[List[Any], Tuple[Any, ...], Set[Any], FrozenSet[Any]]]:
    """Check if something is an iterable collection of items.

    Returns True for list, tuple, set, frozenset, dict views, and other
    Sequence types. Returns False for str, bytes, mappings, generators,
    and scalars."""
    if isinstance(obj, (list, tuple, set, frozenset, MappingView)):
        return True
    return is_sequence(obj)


def unique_list(lst: Iterable[T]) -> List[T]:
    """Remove duplicates from an iterable, retaining order of first appearance.

    Uses dict.fromkeys for hashable items (O(n)). Falls back to a linear
    scan for unhashable items like lists or dicts."""
    try:
        return list(dict.fromkeys(lst))
    except TypeError:
        # unhashable items — fall back to linear scan
        uniq: List[T] = []
        for item in lst:
            if item not in uniq:
                uniq.append(item)
        return uniq


@overload
def ensure_list(obj: None) -> List[Never]:
    pass


@overload
def ensure_list(obj: str) -> List[str]:
    pass


@overload
def ensure_list(obj: bytes) -> List[bytes]:
    pass


@overload
def ensure_list(obj: List[T]) -> List[T]:
    pass


@overload
def ensure_list(obj: Tuple[T, ...]) -> List[T]:
    pass


@overload
def ensure_list(obj: Set[T]) -> List[T]:
    pass


@overload
def ensure_list(obj: FrozenSet[T]) -> List[T]:
    pass


@overload
def ensure_list(obj: T) -> List[T]:
    pass


def ensure_list(obj: Any) -> List[Any]:
    """Normalize uncertain input into a list.

    None returns []. Collections (list, tuple, set, frozenset, dict views,
    etc.) are converted to a list. Strings, bytes, dicts, and
    all other values are wrapped as a single-element list."""
    if obj is None:
        return []
    if is_listish(obj):
        return list(obj)
    return [obj]


def chunked_iter(
    iterable: Iterable[T], batch_size: int = 500
) -> Generator[List[T], None, None]:
    """Yield successive lists of up to ``batch_size`` items from an iterable.

    The final batch may be shorter. Raises ValueError if batch_size < 1."""
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    batch = list()
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = list()
    if len(batch) > 0:
        yield batch


def chunked_iter_sets(
    iterable: Iterable[T], batch_size: int = 500
) -> Generator[Set[T], None, None]:
    """Yield successive sets of up to ``batch_size`` unique items from an iterable.

    Duplicates within a batch reduce the set size without triggering a new
    batch. The final batch may be smaller. Raises ValueError if batch_size < 1."""
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    batch = set()
    for item in iterable:
        batch.add(item)
        if len(batch) >= batch_size:
            yield batch
            batch = set()
    if len(batch) > 0:
        yield batch


@overload
def first(lst: None) -> None:
    pass


@overload
def first(lst: Sequence[T]) -> Optional[T]:
    pass


@overload
def first(lst: T) -> T:
    pass


def first(lst: Any) -> Any:
    """Return the first non-None element, or None if empty.

    Input is passed through ensure_list, so None returns None, scalars
    return themselves, and sequences are searched for the first non-None item."""
    for item in ensure_list(lst):
        if item is not None:
            return item
    return None
