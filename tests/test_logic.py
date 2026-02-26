import pytest
from src.logic import match_pattern, get_evil_outcome, is_hard_mode_compliant, get_updated_keyboard

@pytest.mark.parametrize("guess, secret, expected", [
    # case 1: all correct
    ("CRANE", "CRANE", "22222"),
    # case 2: all wrong
    ("PLUMB", "EXIST", "00000"),
    # case 3: all right letters in wrong positions
    ("WORDS", "SWORD", "11111"),
    # case 4: double letter in guess, word has one
    #expected: first e yellow, second gray
    ("STEER", "STARE", "22101"),
    # case 5: double letter in both guess and word
    # expected: both green
    ("TREES", "STEER", "11221"),
    # case 6: green takes priority over yellow
    # expected: first and last N gray, middle N green
    ("NINNY", "BANJO", "00200"),
    # case 6: guess 5 e's, word has 4
    # expected: first E gray, rest green
    ("EEEEE", "REEEE", "02222")
])
def test_match_pattern_scenarios(guess, secret, expected):
    assert match_pattern(guess, secret) == expected
    
def test_evil_outcome_bucketing(monkeypatch):
    word_pool = ["APPLE", "APPLY", "BEACH"]
    guess = "APPLE"
    
    def mock_choices(population, weights, k):
        return [population[0]]
    
    monkeypatch.setattr("random.choices", mock_choices)
    
    pattern, new_pool = get_evil_outcome(guess, word_pool)
    
    for word in new_pool:
        from src.logic import match_pattern
        assert match_pattern(guess, word) == pattern

def test_evil_outcome_prefers_larger_buckets():
    """Statistical check because can't use normal asserts, since the function has some randomization"""
    word_pool = ["APPLE"] * 10 + ["FUNNY"] * 1
    guess = "FUNNY"
    
    results = []
    for _ in range(100):
        pattern, _ = get_evil_outcome(guess, word_pool)
        results.append(pattern)
    
    apple_count = results.count("00000")
    funny_count = results.count("22222")
    
    assert apple_count > funny_count
    
    # Squared weights, so 10 vs 1 becomes 100 vs 1 -> 10-word bucket should win ~99% of the time
    assert apple_count > 90
    
        
def test_hard_mode_violates_green():
    is_valid, errors = is_hard_mode_compliant("BRAIN", "CRANE", "20000")
    assert is_valid is False
    assert "Must use C at position 1" in errors
    
def test_hard_mode_violates_yellow():
    is_valid, errors = is_hard_mode_compliant("BLOCK", "CRANE", "00100")
    assert is_valid is False
    assert "Must include A" in errors
    
def test_keyboard_status_upgrades():
    kb = {"A": 0}
    # pattern "1" = Yellow -> status becomes 2
    kb = get_updated_keyboard(kb, "a", "1")
    assert kb["A"] == 2
    # pattern "0" (gray) should not downgrade yellow status -> status still 2
    kb = get_updated_keyboard(kb, "A", "0")
    assert kb["A"] == 2
    # pattern "2" (green) should upgrade yellow -> status becomes 3
    kb = get_updated_keyboard(kb, "A", "2")
    assert kb["A"] == 3