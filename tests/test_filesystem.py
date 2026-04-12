from banal.filesystem import decode_path


def test_decode_path_none():
    assert decode_path(None) is None


def test_decode_path_string():
    assert decode_path("/tmp/test.txt") == "/tmp/test.txt"


def test_decode_path_unicode():
    assert decode_path("/tmp/café.txt") == "/tmp/café.txt"
