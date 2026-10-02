# FIXME: Difficulty progression is reversed: Normal should be harder than Easy but easier than Hard.
# We collaborated to fix the difficulty bug by making the ranges scale correctly:
# Easy < Normal < Hard instead of letting Normal become the easiest setting.
def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) range for the requested difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Validate and parse a whole-number guess."""
    # We collaborated to fix the input-validation bug by rejecting invalid
    # guess formats so the app only accepts whole numbers.
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    cleaned = str(raw).strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    try:
        if "." in cleaned or "e" in cleaned.lower():
            raise ValueError
        value = int(cleaned)
    except ValueError:
        return False, None, "That is not a whole number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a guess to the secret number and return the outcome and hint."""
    # We collaborated to fix the high/low bug by making the hint direction match
    # the actual relationship between the guess and the secret number.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess < secret:
        return "Too Low", "📈 Go HIGHER!"
    return "Too High", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update the score based on the outcome and number of attempts."""
    # We collaborated to fix the scoring bug by calculating the score from the
    # actual attempt count instead of letting the round drift out of sync.
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return current_score - 5

    return current_score
