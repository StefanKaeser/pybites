import pytest

from numbers_to_dec import list_to_decimal


def test_type_error_float():
    with pytest.raises(TypeError):
        list_to_decimal([1.1])


def test_type_error_bool():
    with pytest.raises(TypeError):
        list_to_decimal([True])


def test_value_error_negative():
    with pytest.raises(ValueError):
        list_to_decimal([-1])


def test_value_error_gt_9():
    with pytest.raises(ValueError):
        list_to_decimal([10])


@pytest.mark.parametrize("test_input,expected", [([1, 7, 5], 175), ([0, 3, 1, 2], 312)])
def test_examples(test_input, expected):
    assert list_to_decimal(test_input) == expected
