from datetime import date, datetime

from banal.cache import bytes_iter, hash_data


# bytes_iter


def test_bytes_iter_none():
    assert list(bytes_iter(None)) == []


def test_bytes_iter_string():
    assert list(bytes_iter("hello")) == [b"hello"]


def test_bytes_iter_bytes():
    assert list(bytes_iter(b"hello")) == [b"hello"]


def test_bytes_iter_int():
    assert list(bytes_iter(42)) == [b"42"]


def test_bytes_iter_date():
    d = date(2024, 1, 15)
    assert list(bytes_iter(d)) == [b"2024-01-15"]


def test_bytes_iter_datetime():
    dt = datetime(2024, 1, 15, 12, 30, 0)
    assert list(bytes_iter(dt)) == [b"2024-01-15T12:30:00"]


def test_bytes_iter_list():
    # lists get sorted
    result = list(bytes_iter([2, 1, 3]))
    assert result == [b"1", b"2", b"3"]


def test_bytes_iter_dict():
    # dicts iterate sorted keys then values
    result = list(bytes_iter({"b": 2, "a": 1}))
    assert result == [b"a", b"1", b"b", b"2"]


def test_bytes_iter_nested():
    result = list(bytes_iter({"key": [1, 2]}))
    assert result == [b"key", b"1", b"2"]


def test_bytes_iter_dict_not_mutated():
    d = {None: "x", "a": 1}
    list(bytes_iter(d))
    assert None in d


def test_bytes_iter_function():
    def my_func():
        pass

    result = list(bytes_iter(my_func))
    assert result == [b"my_func"]


# hash_data


def test_hash_data_deterministic():
    assert hash_data({"a": 1}) == hash_data({"a": 1})


def test_hash_data_different_values():
    assert hash_data({"a": 1}) != hash_data({"a": 2})


def test_hash_data_key_order_irrelevant():
    assert hash_data({"a": 1, "b": 2}) == hash_data({"b": 2, "a": 1})


def test_hash_data_none():
    result = hash_data(None)
    # SHA1 of empty input
    assert isinstance(result, str)
    assert len(result) == 40


def test_hash_data_string():
    result = hash_data("hello")
    assert isinstance(result, str)
    assert len(result) == 40


def test_hash_data_returns_hex():
    result = hash_data("test")
    int(result, 16)  # should not raise
