from logic_utils import check_guess

def test_winning_guess():
    outcome, hint = check_guess(50, 50)
    assert outcome == "Win"
    assert hint == "🎉 Correct!"

def test_guess_too_high():
    outcome, hint = check_guess(60, 50)
    assert outcome == "Too High"
    assert hint == "📉 Go LOWER!"

def test_guess_too_low():
    outcome, hint = check_guess(3, 40)
    assert outcome == "Too Low"
    assert hint == "📈 Go HIGHER!"
