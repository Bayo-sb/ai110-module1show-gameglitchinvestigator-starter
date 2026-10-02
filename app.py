import random
import streamlit as st


def get_range_for_difficulty(difficulty: str):
    # We collaborated to fix the difficulty bug by making the ranges scale correctly:
    # Easy < Normal < Hard instead of letting Normal become the easiest setting.
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
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


def check_guess(guess, secret):
    # We collaborated to fix the high/low bug by making the hint direction match
    # the actual relationship between the guess and the secret number.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess < secret:
        return "Too Low", "📈 Go HIGHER!"
    return "Too High", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    # We collaborated to fix the scoring bug by calculating the score from the
    # actual attempt count instead of letting the round drift out of sync.
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return current_score - 5

    return current_score


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 5,
    "Hard": 4,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# We collaborated to fix the stale-state bug by clearing every value
# before starting a new round, so the secret number and score do not leak.
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(attempt_limit - st.session_state.attempts, 0)}"
)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # We collaborated to fix the new-game reset bug by making sure the old
    # session data is cleared before the next round starts.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    # We collaborated to fix the input validation bug by checking the parsed
    # number before comparing it to the secret.
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
        st.stop()

    if guess_int < low or guess_int > high:
        st.error(f"Guess out of range. Enter a number between {low} and {high}.")
        st.stop()

    st.session_state.attempts += 1
    st.session_state.history.append(guess_int)

    outcome, message = check_guess(guess_int, st.session_state.secret)

    if show_hint:
        st.warning(message)

    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    if outcome == "Win":
        st.balloons()
        st.session_state.status = "won"
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
