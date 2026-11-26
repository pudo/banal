import os

import pytest

from banal.filesystem import decode_path


def test_decode_path_none():
    assert decode_path(None) is None


def test_decode_path_string():
    assert decode_path("/tmp/test.txt") == "/tmp/test.txt"


def test_decode_path_unicode():
    assert decode_path("/tmp/café.txt") == "/tmp/café.txt"


def test_decode_path_bytes():
    path = "/tmp/café.txt"
    assert decode_path(os.fsencode(path)) == path


def test_decode_path_filesystem_error_handler():
    path = "/tmp/test-\udcff.txt"
    assert decode_path(os.fsencode(path)) == path


@pytest.mark.skipif(os.name != "posix", reason="Raw byte filenames require POSIX")
def test_decode_path_non_utf8_filename(tmp_path):
    raw_path = os.fsencode(tmp_path) + b"/test-\xff.txt"
    with open(raw_path, "wb") as stream:
        stream.write(b"payload")

    path = decode_path(raw_path)

    assert isinstance(path, str)
    assert os.fsencode(path) == raw_path
    with open(path, "rb") as stream:
        assert stream.read() == b"payload"
