import random

import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


DIFFICULTY_OPTIONS = ["Easy", "Normal", "Hard"]
ATTEMPT_LIMITS = {"Easy": 6, "Normal": 5, "Hard": 4}


def reset_round(difficulty: str, low: int, high: int) -> None:
    """Reset game state for a fresh round."""
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""


def initialize_session_state(difficulty: str, low: int, high: int) -> None:
    """Ensure session state is ready for the selected difficulty."""
    if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
        reset_round(difficulty, low, high)

    defaults = {
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "guess_input": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    DIFFICULTY_OPTIONS,
    index=1,
)

attempt_limit = ATTEMPT_LIMITS[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

initialize_session_state(difficulty, low, high)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(attempt_limit - st.session_state.attempts, 0)}"
)

with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        value=st.session_state.guess_input,
    )
    submit = st.form_submit_button("Submit Guess 🚀")
    new_game = st.form_submit_button("New Game 🔁")
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_round(difficulty, low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)
    st.session_state.guess_input = raw_guess

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

st.sidebar.markdown("### Developer Debug Info")
st.sidebar.write("secret:", st.session_state.get("secret"))
st.sidebar.write("attempts:", st.session_state.get("attempts"))
st.sidebar.write("status:", st.session_state.get("status"))
st.sidebar.write("score:", st.session_state.get("score"))
st.sidebar.write("history:", st.session_state.get("history"))

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
