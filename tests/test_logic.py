import pytest
import random
from src.logic import match_pattern, get_evil_outcome

@pytest.mark.parametrize("guess, secret, expected", [
    #case 1: all correct
    ("CRANE", "CRANE", "22222"),
    #case 2: all wrong
    ("PLUMB", "EXIST", "00000"),
    #case 3: all right letters in wrong positions
    ("WORDS", "SWORD", "11111"),
    #case 4: double letter in guess, word has one
    #expected: first e yellow, second gray
    ("STEER", "STARE", "22101"),
    #case 5: double letter in both guess and word
    #expected: both green
    ("TREES", "STEER", "11221"),
    #case 6: green takes priority over yellow
    #expected: first and last N gray, middle N green
    ("NINNY", "BANJO", "00200"),
])
def test_match_pattern_scenarios(guess, secret, expected):
    assert match_pattern(guess, secret) == expected
    
def test_evil_outcome_prefers_larger_buckets():
    """Statistical check because can't use normal asserts, since the function has some randomization"""
    word_pool = ["APPLE"] * 10 + ["HORSE"] * 1
    guess = "APPLE"
    
    results = []
    for _ in range(100):
        pattern, _ = get_evil_outcome(guess, word_pool)
        results.append(pattern)
        
    apple_count = results.count("22222")
    zorro_count = results.count("00000")
    
    assert apple_count > zorro_count
    
    # Squared weights, so 10 vs 1 becomes 100 vs 1 -> 10-word bucket should win ~99% of the time
    assert apple_count > 90