from unittest.mock import patch

import pytest

import color


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


@patch("color.sample")
def test_gen_hex_color(mock_sample, gen):
    mock_sample.return_value = 1, 2, 3
    assert next(gen) == "#010203"
    mock_sample.assert_called_with(range(0, 256), 3)
