from banal.bools import as_bool


def test_as_bool_true():
    assert as_bool(True) is True


def test_as_bool_false():
    assert as_bool(False) is False


def test_as_bool_none_default_false():
    assert as_bool(None) is False


def test_as_bool_none_default_true():
    assert as_bool(None, default=True) is True


def test_as_bool_truthy_strings():
    for val in ["1", "yes", "y", "t", "true", "on", "enabled"]:
        assert as_bool(val) is True, f"expected True for {val!r}"


def test_as_bool_truthy_strings_case_insensitive():
    for val in ["Yes", "YES", "True", "TRUE", "ON"]:
        assert as_bool(val) is True, f"expected True for {val!r}"


def test_as_bool_truthy_strings_whitespace():
    assert as_bool("  yes  ") is True


def test_as_bool_falsy_strings():
    for val in ["0", "no", "false", "off", "disabled", "nope"]:
        assert as_bool(val) is False, f"expected False for {val!r}"


def test_as_bool_empty_string_default_false():
    assert as_bool("") is False


def test_as_bool_empty_string_default_true():
    assert as_bool("", default=True) is True


def test_as_bool_int_one():
    assert as_bool(1) is True


def test_as_bool_int_zero():
    assert as_bool(0) is False


def test_as_bool_int_other():
    # "42" is not in BOOL_TRUEISH
    assert as_bool(42) is False
