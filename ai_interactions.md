# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Copilot to fix the input parsing logic so the game only accepted valid whole-number guesses. I specifically wanted it to reject empty input, `None` values, whitespace-only strings, decimals like `3.5`, scientific notation like `1e3`, and non-numeric text like `abc`. The goal was to make the app reject malformed input cleanly and keep the parsing behavior consistent and testable.

**What did the agent do?**

The agent reviewed the parsing helper and updated the validation logic so it only accepted valid whole-number guesses. It also added focused pytest checks for malformed inputs and verified that the edge cases were handled consistently. I specifically asked it to handle:
- empty strings
- `None`
- whitespace-only input
- decimals like `3.5`
- scientific notation like `1e3`
- non-numeric text like `abc`

It then adjusted the `parse_guess` function and tests so those cases returned the expected error messages instead of crashing or accepting invalid values.

**What did you have to verify or fix manually?**

I verified the parsing behavior in the game logic and confirmed the edge cases were handled correctly in pytest. I also checked that the error messages matched the project’s expected wording and that the validation stayed consistent across malformed inputs.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Empty string | “Write a pytest case for parse_guess that rejects an empty string.” | `assert parse_guess("") == (False, None, "Enter a guess.")` | Yes | It confirms blank input is rejected cleanly. |
| None input | “Add a pytest case for None in parse_guess.” | `assert parse_guess(None) == (False, None, "Enter a guess.")` | Yes | It prevents crashes from missing input. |
| Whitespace-only input | “Add a test for spaces-only input.” | `assert parse_guess("   ") == (False, None, "Enter a guess.")` | Yes | It catches accidental spaces being treated as guesses. |
| Decimal input | “Reject decimals like 3.5.” | `assert parse_guess("3.5") == (False, None, "That is not a whole number.")` | Yes | Validates that only whole numbers are accepted. |
| Scientific notation | “Reject 1e3 in parse_guess.” | `assert parse_guess("1e3") == (False, None, "That is not a whole number.")` | Yes | Stops invalid scientific notation from slipping through. |
| Non-numeric text | “Reject non-numeric input like abc.” | `assert parse_guess("abc") == (False, None, "That is not a whole number.")` | Yes | Keeps the app from accepting garbage input. |

---

## Linting & Style (SF9)

I asked Copilot to simplify the app structure and make the code easier to read without changing the logic. It suggested:
- moving repeated game logic into helper functions
- keeping session-state initialization in one place
- separating reset logic from gameplay logic
- preserving the same behavior while improving readability
- keeping comments clear and concise

I accepted the changes that improved readability and did not change game rules or app behavior. The final version keeps the same functionality while making the code easier to scan and maintain.

**Prompt used:**

```
Go through my code and ensure standard practice with PEP 8 style and make it readable without breaking my code.
```

**Linting output before:**

```
None
```

**Changes applied:**

I accepted the refactor that kept the same gameplay behavior while making the app easier to scan and maintain. The final version uses helper functions to initialize and reset session state, keeps the logic organized, and preserves the original rules of the game without changing how it plays.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
