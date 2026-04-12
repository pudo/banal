import pytest

from banal.lists import (
    is_sequence,
    is_listish,
    ensure_list,
    unique_list,
    chunked_iter,
    chunked_iter_sets,
    first,
)


# is_sequence


def test_is_sequence_list():
    assert is_sequence([1, 2]) is True


def test_is_sequence_tuple():
    assert is_sequence((1, 2)) is True


def test_is_sequence_string():
    assert is_sequence("hello") is False


def test_is_sequence_bytes():
    assert is_sequence(b"hello") is False


def test_is_sequence_int():
    assert is_sequence(42) is False


def test_is_sequence_none():
    assert is_sequence(None) is False


def test_is_sequence_dict():
    assert is_sequence({"a": 1}) is False


def test_is_sequence_set():
    # set is not a Sequence
    assert is_sequence({1, 2}) is False


def test_is_sequence_range():
    assert is_sequence(range(5)) is True


# is_listish


def test_is_listish_list():
    assert is_listish([1, 2]) is True


def test_is_listish_tuple():
    assert is_listish((1, 2)) is True


def test_is_listish_set():
    assert is_listish({1, 2}) is True


def test_is_listish_string():
    assert is_listish("hello") is False


def test_is_listish_bytes():
    assert is_listish(b"hello") is False


def test_is_listish_dict():
    assert is_listish({"a": 1}) is False


def test_is_listish_int():
    assert is_listish(42) is False


def test_is_listish_none():
    assert is_listish(None) is False


def test_is_listish_generator():
    assert is_listish(x for x in [1]) is False


def test_is_listish_range():
    assert is_listish(range(5)) is True


def test_is_listish_frozenset():
    assert is_listish(frozenset({1, 2})) is True


def test_is_listish_dict_keys():
    assert is_listish({"a": 1, "b": 2}.keys()) is True


def test_is_listish_dict_values():
    assert is_listish({"a": 1, "b": 2}.values()) is True


def test_is_listish_dict_items():
    assert is_listish({"a": 1}.items()) is True


def test_is_listish_empty_list():
    assert is_listish([]) is True


def test_is_listish_empty_set():
    assert is_listish(set()) is True


# ensure_list


def test_ensure_list_none():
    assert ensure_list(None) == []


def test_ensure_list_list():
    assert ensure_list([1, 2, 3]) == [1, 2, 3]


def test_ensure_list_tuple():
    assert ensure_list((1, 2)) == [1, 2]


def test_ensure_list_set():
    result = ensure_list({1})
    assert result == [1]


def test_ensure_list_string():
    assert ensure_list("hello") == ["hello"]


def test_ensure_list_bytes():
    assert ensure_list(b"hello") == [b"hello"]


def test_ensure_list_int():
    assert ensure_list(42) == [42]


def test_ensure_list_dict():
    d = {"a": 1}
    assert ensure_list(d) == [d]


def test_ensure_list_empty_list():
    assert ensure_list([]) == []


def test_ensure_list_nested_list():
    assert ensure_list([[1, 2], [3]]) == [[1, 2], [3]]


def test_ensure_list_bool():
    assert ensure_list(True) == [True]


def test_ensure_list_zero():
    assert ensure_list(0) == [0]


def test_ensure_list_empty_string():
    assert ensure_list("") == [""]


def test_ensure_list_frozenset():
    result = ensure_list(frozenset({1}))
    assert result == [1]


def test_ensure_list_dict_keys():
    result = ensure_list({"a": 1, "b": 2}.keys())
    assert set(result) == {"a", "b"}


def test_ensure_list_dict_values():
    result = ensure_list({"a": 1, "b": 2}.values())
    assert set(result) == {1, 2}


# unique_list


def test_unique_list_duplicates():
    assert unique_list([1, 2, 2, 3, 1]) == [1, 2, 3]


def test_unique_list_no_duplicates():
    assert unique_list([1, 2, 3]) == [1, 2, 3]


def test_unique_list_empty():
    assert unique_list([]) == []


def test_unique_list_preserves_order():
    assert unique_list([3, 1, 2, 1, 3]) == [3, 1, 2]


def test_unique_list_strings():
    assert unique_list(["a", "b", "a"]) == ["a", "b"]


def test_unique_list_unhashable():
    assert unique_list([[1], [2], [1]]) == [[1], [2]]


def test_unique_list_single():
    assert unique_list([1]) == [1]


# chunked_iter


def test_chunked_iter_exact_batches():
    result = list(chunked_iter([1, 2, 3, 4], batch_size=2))
    assert result == [[1, 2], [3, 4]]


def test_chunked_iter_remainder():
    result = list(chunked_iter([1, 2, 3, 4, 5], batch_size=2))
    assert result == [[1, 2], [3, 4], [5]]


def test_chunked_iter_empty():
    assert list(chunked_iter([], batch_size=2)) == []


def test_chunked_iter_single_batch():
    result = list(chunked_iter([1, 2], batch_size=10))
    assert result == [[1, 2]]


def test_chunked_iter_batch_size_one():
    result = list(chunked_iter([1, 2, 3], batch_size=1))
    assert result == [[1], [2], [3]]


def test_chunked_iter_generator_input():
    result = list(chunked_iter(range(5), batch_size=2))
    assert result == [[0, 1], [2, 3], [4]]


def test_chunked_iter_zero_batch_size():
    with pytest.raises(ValueError):
        list(chunked_iter([1, 2], batch_size=0))


def test_chunked_iter_negative_batch_size():
    with pytest.raises(ValueError):
        list(chunked_iter([1, 2], batch_size=-1))


# chunked_iter_sets


def test_chunked_iter_sets_exact_batches():
    result = list(chunked_iter_sets([1, 2, 3, 4], batch_size=2))
    assert result == [{1, 2}, {3, 4}]


def test_chunked_iter_sets_remainder():
    result = list(chunked_iter_sets([1, 2, 3, 4, 5], batch_size=2))
    assert result == [{1, 2}, {3, 4}, {5}]


def test_chunked_iter_sets_empty():
    assert list(chunked_iter_sets([], batch_size=2)) == []


def test_chunked_iter_sets_duplicates_shrink_batch():
    # Duplicates within a batch don't count toward batch_size
    result = list(chunked_iter_sets([1, 1, 1, 2, 3], batch_size=2))
    assert result == [{1, 2}, {3}]


def test_chunked_iter_sets_zero_batch_size():
    with pytest.raises(ValueError):
        list(chunked_iter_sets([1, 2], batch_size=0))


def test_chunked_iter_sets_negative_batch_size():
    with pytest.raises(ValueError):
        list(chunked_iter_sets([1, 2], batch_size=-1))


# first


def test_first_basic():
    assert first([1, 2, 3]) == 1


def test_first_skips_none():
    assert first([None, None, 3]) == 3


def test_first_all_none():
    assert first([None, None]) is None


def test_first_empty():
    assert first([]) is None


def test_first_none_input():
    assert first(None) is None


def test_first_string_input():
    assert first("hello") == "hello"


def test_first_int_input():
    assert first(42) == 42
