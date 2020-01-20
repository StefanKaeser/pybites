from unittest.mock import patch

import pytest

from guess import GuessGame, InvalidNumber


@pytest.mark.parametrize("test_input", [0, 1, 2, 9, 11, 15])
def test_validation_number(test_input):
    game = GuessGame(secret_number=test_input)
    assert game.secret_number == test_input


@pytest.mark.parametrize("test_input", ["str"])
def test_validation_not_a_number(test_input):
    with pytest.raises(InvalidNumber, match="Not a number"):
        GuessGame(secret_number=test_input)


@pytest.mark.parametrize("test_input", [-1, -2, -9, -11])
def test_validation_negative_number(test_input):
    with pytest.raises(InvalidNumber, match="Negative number"):
        GuessGame(secret_number=test_input)


@pytest.mark.parametrize("test_input", [16, 32, 101])
def test_validation_number_too_high(test_input):
    with pytest.raises(InvalidNumber, match="Number too high"):
        GuessGame(secret_number=test_input)


def test_max_guesses_default():
    game = GuessGame(secret_number=1)
    assert game.max_guesses == 5


@pytest.mark.parametrize("test_input", [16, 32, 101])
def test_max_guesses(test_input):
    game = GuessGame(secret_number=1, max_guesses=test_input)
    assert game.max_guesses == test_input


def test_starts_at_zero_attempts():
    game = GuessGame(secret_number=1)
    assert game.attempt == 0


@patch("guess.input")
def test_guess_number(mock_input, capfd):
    game = GuessGame(secret_number=10)
    mock_input.side_effect = [1, 9, 13, 11, 10]
    game()
    output = capfd.readouterr()[0].splitlines()
    assert output == [
        "Guess a number: ",
        "Too low",
        "Guess a number: ",
        "Too low",
        "Guess a number: ",
        "Too high",
        "Guess a number: ",
        "Too high",
        "Guess a number: ",
        "You guessed it!",
    ]
    assert game.attempt == 5


@patch("guess.input")
def test_too_many_attempts(mock_input, capfd):
    game = GuessGame(secret_number=10)
    mock_input.side_effect = [1, 9, 13, 12, 11]
    game()
    output = capfd.readouterr()[0].splitlines()
    assert output == [
        "Guess a number: ",
        "Too low",
        "Guess a number: ",
        "Too low",
        "Guess a number: ",
        "Too high",
        "Guess a number: ",
        "Too high",
        "Guess a number: ",
        "Too high",
        "Sorry, the number was 10",
    ]


@patch("guess.input")
def test_entered_not_a_number(mock_input, capfd):
    game = GuessGame(secret_number=10)
    mock_input.side_effect = ["string", 10]
    game()
    output = capfd.readouterr()[0].splitlines()
    assert output == [
        "Guess a number: ",
        "Enter a number, try again",
        "Guess a number: ",
        "You guessed it!",
    ]
    assert game.attempt == 1
