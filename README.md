# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

This game is a number-guessing app built in Streamlit. The player chooses a difficulty level, tries to guess a secret whole number within a range, and receives feedback until they either win or run out of attempts.

The main bugs I found were the reversed hint logic, stale game state between rounds, incorrect difficulty progression, and invalid guesses being accepted without proper range checks. The hints were telling players to go lower when the guess was too low, and the game was not resetting cleanly when a new round started.

I fixed the comparison logic so lower guesses correctly say “Go HIGHER!” and higher guesses correctly say “Go LOWER!” I also corrected the difficulty ranges, reset stale session state on new games and difficulty changes, and added validation so the app rejects invalid input and guesses outside the allowed range. I moved the reusable logic into `logic_utils.py` and verified the behavior with pytest.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

Open the app and choose a difficulty level: Easy, Normal, or Hard. The game generates a secret whole number within the chosen range.

Enter a guess in the text box and click Submit. The app checks whether the value is valid and whether it is within the allowed range for that difficulty.

The game compares your guess to the secret number using numeric logic and decides whether the answer is too low or too high.

The app gives a clear hint: if your guess is too low, it tells you to go higher, and if it is too high, it tells you to go lower.

Keep guessing until you either find the secret number or run out of attempts. The score updates after each guess, and you can start a new round at any time.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```bash
pytest -q test/test_game_logic.py
========================
18 passed in 0.02s
========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
