import random
from collections import Counter

#returns a pattern match string "XXXXX" for a guessed word relative to a single word in the list, where 0 = grey 1 = yellow 2 = green
def match_pattern(guess, word):
    count = Counter(word)
    pattern = ["0"] * len(guess)
    
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

#adds each pattern to a bucket, then weightedly picks a pattern and returns it and the associated word list
def get_evil_outcome(guess, word_pool):
    buckets = {}
    
    for word in word_pool:
        pattern = match_pattern(guess, word)
        buckets.setdefault(pattern, []).append(word)
        
    
    patterns = []
    weights = []
    for pattern, words in buckets.items():
        patterns.append(pattern)
        weights.append(len(words)**2)

    chosen_pattern = random.choices(patterns, weights=weights, k=1)[0]
    
    return chosen_pattern, buckets[chosen_pattern]

def is_hard_mode_compliant(current_guess, last_guess, last_pattern):
    if not last_guess or not last_pattern:
        return True, []
    
    errors = []
    
    for i, char in enumerate(last_pattern):
        if char == "2":
            if current_guess[i] != last_guess[i]:
                errors.append(f"Must use {last_guess[i]} at position {i + 1}")
        
        elif char == "1":
            if last_guess[i] not in current_guess:
                errors.append(f"Must include {last_guess[i]}")
                
    if not errors:
        return True, []
    
    return False, errors

def get_updated_keyboard(current_keyboard, guess, pattern):
    
    new_keyboard = current_keyboard.copy()
    
    for i, char in enumerate(guess.upper()):
        if char not in new_keyboard:
            continue
        
        new_status = int(pattern[i]) + 1
        
        if new_status > new_keyboard[char]:
            new_keyboard[char] = new_status
        
    return new_keyboard
        