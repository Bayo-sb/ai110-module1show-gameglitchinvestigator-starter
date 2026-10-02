import random
import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


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

# We collaborated to fix the stale-state bug by resetting the session whenever the difficulty changes.
# FIXME: Difficulty resets must clear stale session state.
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""

# We collaborated to fix the missing-state bug by initializing the session values before the game begins.
# FIXME: Fresh sessions must initialize all required state.
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

# We collaborated to fix the new-game reset bug by clearing the previous round before starting fresh.
# FIXME: New game must clear previous state before starting a fresh round.
if new_game:
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
    # We collaborated to fix the range-validation bug by rejecting guesses outside the active difficulty.
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
        st.stop()

    # FIXME: Out-of-range guesses must be rejected before comparing values.
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

st.sidebar.markdown("### Developer Debug Info")
st.sidebar.write("secret:", st.session_state.get("secret"))
st.sidebar.write("attempts:", st.session_state.get("attempts"))
st.sidebar.write("status:", st.session_state.get("status"))
st.sidebar.write("score:", st.session_state.get("score"))
st.sidebar.write("history:", st.session_state.get("history"))

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
