# FIXME: Difficulty progression is reversed: Normal should be harder than Easy but easier than Hard.
# We collaborated to fix the difficulty bug by making the ranges scale correctly:
# Easy < Normal < Hard instead of letting Normal become the easiest setting.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # We collaborated to fix the input bug by rejecting decimals and scientific notation.
    # FIXME: This validator must reject decimals and scientific notation.
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


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # We collaborated to fix the comparison bug by keeping values numeric and
    # making the hint direction match the actual relationship: low => go higher.
    # FIXME: Do not compare strings here; keep everything numeric.
    # FIXME: Hint direction is reversed here; too-low guesses should say to go higher.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess < secret:
        return "Too Low", "📈 Go HIGHER!"
    return "Too High", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # We collaborated to fix the scoring bug by making it depend on the real attempt count.
    # FIXME: Score should be consistent and based on the real attempt count.
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return current_score - 5

    return current_score
