import pytest


def f():
    raise KeyError


def test_f():
    with pytest.raises(KeyError):
        f()