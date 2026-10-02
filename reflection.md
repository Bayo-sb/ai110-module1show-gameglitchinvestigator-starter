# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").



There were obvious error as I ran the game
First Bug: I noticed that the hint contradicted the actual result.
Second Bug: At the end of the game, clicking “New Game” does not reset the game to its default state.
Third Bug: Normal difficulty mode is much easier than easy mode because it allows more attempts and has the same    range of numbers to guess.
Fourth Bug: Pressing the Enter key reduces the number of attempts without recording the attempt in the history.
Fifth Bug: It allows numbers outside the range.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|---|---|---|---|
| Guess 5 with a secret of 17 | The hint should say to go higher | The app told me to go lower | None |
| Guess 189 in Easy mode | The game should reject it as out of range | It allowed the guess to run | None |
| Click “New Game” at the end of the game | The game should reset to its default state | The game did not reset properly | None |
| Select Normal difficulty | Normal should be harder than Easy | Normal was easier than Easy and used the same number range | None |
| Enter a guess and press Enter | The guess should be counted and recorded | The number of attempts decreased without adding the guess to the history | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used GitHub Copilot in VS Code on this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One AI suggestion that was correct was the diagnosis of the hint bug: it pointed out that the comparison function was returning the wrong instruction for low and high guesses. I verified it by checking a few inputs directly, such as guess 3 with secret 40, which should say “Go HIGHER!”, and guess 60 with secret 50, which should say “Go LOWER!”.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

One suggestion I did not accept as written was a broader refactor of the app state and input flow. The AI proposed changing more of the Streamlit logic than necessary, and I rejected that because it was harder to read and more likely to create new regressions.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tested it on the streamlit app
- Describe at least one test you ran (manual or using pytest)  

I ran a manual test where the secret was 17 and the guess was 10. The correct hint should say “Go HIGHER!”, but the app initially said the opposite, which showed that the hint logic was reversed. I also ran pytest for the logic functions, and it confirmed that the fix for the hint direction, difficulty ranges, and input validation worked as expected.

- Did AI help you design or understand any tests? How?
Yes, AI helped me design smaller, more focused tests for the logic functions. Instead of testing the whole app at once
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit has to be refreshed every time to ensure the changes have been implemented. I also had to use Ctrl+C to disconnect from the existing session before rerunning it.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

The way I tested each AI suggestion with real examples before moving on to the next bug.

- What is one thing you would do differently next time you work with AI on a coding task?

Try bettter to understand the code before I proceed

- In one or two sentences, describe how this project changed the way you think about AI generated code.
It is a good partner that must be crosscheck evey time
