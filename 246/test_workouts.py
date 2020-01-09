import pytest

from workouts import print_workout_days


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("upper", "Mon, Thu\n"),
        ("upper body #1", "Mon\n"),
        ("upper body #2", "Thu\n"),
        ("cardio", "Wed\n"),
        ("lower", "Tue, Fri\n"),
        ("lower body #1", "Tue\n"),
        ("lower body #2", "Fri\n"),
        ("bogus", "No matching workout\n"),
    ],
)
def test_print_workout_days(capfd, test_input, expected):
    print_workout_days(test_input)
    out, _ = capfd.readouterr()
    assert out == expected
