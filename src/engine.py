import random
from collections import Counter

def match_pattern(guess, word):
    count = Counter(word)
    pattern = ["0"] * 5
    for i in range(len(guess)):
        letter = guess[i]
        if letter == word[i]:
            pattern[i] = "2"
            count[letter] -= 1
    for i in range(len(guess)):
        letter = guess[i]
        if pattern[i] == "2":
            continue
        if count[letter] > 0:
            pattern[i] = "1"
            count[letter] -= 1
    return "".join(pattern)

def get_best_outcome(guess, word_pool):
    buckets = {}
    
    for word in word_pool:
        pattern = match_pattern(guess, word)
        if pattern not in buckets:
            buckets[pattern] = []
        buckets[pattern].append(word)
    
    sorted_buckets = sorted(buckets.items(), key=lambda x: len(x[1]), reverse=True)
        
    patterns = [p for p, words in sorted_buckets]
    weights = [len(words)**2 for p, words in sorted_buckets]
    
    chosen_pattern = random.choices(patterns, weights=weights, k=1)[0]
    chosen_words = buckets[chosen_pattern]
    
    return chosen_pattern, buckets[chosen_pattern]
        