from collections import OrderedDict

from banal.dicts import is_mapping, ensure_dict, clean_dict, keys_values


# is_mapping


def test_is_mapping_dict():
    assert is_mapping({"a": 1}) is True


def test_is_mapping_ordered_dict():
    assert is_mapping(OrderedDict()) is True


def test_is_mapping_list():
    assert is_mapping([1, 2]) is False


def test_is_mapping_none():
    assert is_mapping(None) is False


def test_is_mapping_string():
    assert is_mapping("hello") is False


# ensure_dict


def test_ensure_dict_dict():
    assert ensure_dict({"a": 1}) == {"a": 1}


def test_ensure_dict_ordered_dict():
    od = OrderedDict([("a", 1), ("b", 2)])
    assert ensure_dict(od) == {"a": 1, "b": 2}


def test_ensure_dict_none():
    assert ensure_dict(None) == {}


def test_ensure_dict_list():
    assert ensure_dict([1, 2]) == {}


def test_ensure_dict_string():
    assert ensure_dict("hello") == {}


def test_ensure_dict_int():
    assert ensure_dict(42) == {}


# clean_dict


def test_clean_dict_removes_none_values():
    assert clean_dict({"a": 1, "b": None}) == {"a": 1}


def test_clean_dict_recursive():
    data = {"a": {"b": None, "c": 2}, "d": None}
    assert clean_dict(data) == {"a": {"c": 2}}


def test_clean_dict_cleans_lists():
    data = {"a": [1, None, 3]}
    assert clean_dict(data) == {"a": [1, 3]}


def test_clean_dict_empty():
    assert clean_dict({}) == {}


def test_clean_dict_no_none():
    assert clean_dict({"a": 1, "b": 2}) == {"a": 1, "b": 2}


def test_clean_dict_all_none():
    assert clean_dict({"a": None, "b": None}) == {}


def test_clean_dict_non_dict_passthrough():
    assert clean_dict(42) == 42
    assert clean_dict("hello") == "hello"


def test_clean_dict_nested_list_of_dicts():
    data = {"items": [{"a": 1, "b": None}, {"c": None}]}
    assert clean_dict(data) == {"items": [{"a": 1}, {}]}


# keys_values


def test_keys_values_single_key():
    assert keys_values({"a": 1}, "a") == [1]


def test_keys_values_missing_key():
    assert keys_values({"a": 1}, "b") == []


def test_keys_values_fallback_keys():
    assert keys_values({"b": 2}, "a", "b") == [2]


def test_keys_values_multiple_matching_keys():
    assert keys_values({"a": 1, "b": 2}, "a", "b") == [1, 2]


def test_keys_values_list_value():
    assert keys_values({"a": [1, 2]}, "a") == [1, 2]


def test_keys_values_non_mapping():
    assert keys_values("hello", "a") == []


def test_keys_values_empty_dict():
    assert keys_values({}, "a") == []


def test_keys_values_none_value():
    result = keys_values({"a": None}, "a")
    assert result == []
