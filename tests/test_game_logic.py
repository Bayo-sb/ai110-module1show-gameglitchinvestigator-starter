import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


@pytest.mark.parametrize(
    "difficulty, expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 50)),
        ("Hard", (1, 100)),
        ("Unknown", (1, 100)),
    ],
)
def test_get_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize(
    "raw, expected_ok, expected_value, expected_msg",
    [
        ("42", True, 42, None),
        (" 7 ", True, 7, None),
        ("", False, None, "Enter a guess."),
        (None, False, None, "Enter a guess."),
        ("3.5", False, None, "That is not a whole number."),
        ("1e3", False, None, "That is not a whole number."),
        ("abc", False, None, "That is not a whole number."),
    ],
)
def test_parse_guess(raw, expected_ok, expected_value, expected_msg):
    ok, value, msg = parse_guess(raw)
    assert ok is expected_ok
    assert value == expected_value
    assert msg == expected_msg


@pytest.mark.parametrize(
    "guess, secret, expected_outcome, expected_msg",
    [
        (50, 50, "Win", "🎉 Correct!"),
        (45, 76, "Too Low", "📈 Go HIGHER!"),
        (90, 76, "Too High", "📉 Go LOWER!"),
        (3, 40, "Too Low", "📈 Go HIGHER!"),
    ],
)
def test_check_guess_numeric_logic(guess, secret, expected_outcome, expected_msg):
    outcome, msg = check_guess(guess, secret)
    assert outcome == expected_outcome
    assert msg == expected_msg


def test_update_score_for_win_and_loss():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 5) == 60
    assert update_score(20, "Too Low", 1) == 15
    assert update_score(20, "Too High", 2) == 15


def test_guess_hint_direction_is_correct_for_low_and_high_guesses():
    outcome, hint = check_guess(3, 40)
    assert outcome == "Too Low"
    assert hint == "📈 Go HIGHER!"

    outcome, hint = check_guess(60, 50)
    assert outcome == "Too High"
    assert hint == "📉 Go LOWER!"


def test_range_rejects_out_of_bounds_guess():
    ok, value, msg = parse_guess("999")
    assert ok is True
    assert value == 999
    assert msg is None

    # Range check must be enforced in the app layer, not the helper.
    # This test documents that non-range-safe values are allowed by parse_guess
    # and must be rejected by the app before processing.