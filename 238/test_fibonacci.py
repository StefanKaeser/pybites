import pytest

from fibonacci import fib


def test_negative():
    with pytest.raises(ValueError):
        fib(-1)


@pytest.mark.parametrize("test_input,expected", [(0, 0), (1, 1), (9, 34)])
def test_positive(test_input, expected):
    assert fib(test_input) == expected
