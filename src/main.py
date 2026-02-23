from src.utils import load_words
from src.engine import get_best_outcome

def main():
    word_pool = load_words("data/solutions.txt")
    valid_words = set(load_words("data/allowed.txt"))
    
    valid_words.update(word_pool)
    
    turns = 0
    max_turns = 6
    
    print("Welcome to Just Wordle\n This is just a normal wordlelike with nothing evil going on.")
    print(f"I'm thinking of one of {len(word_pool)} words...")
    
    while turns < max_turns:
        guess = input(f"\nTurn {turns + 1} - Enter guess: ").strip().upper()
        if guess == "!HINT":
            print(word_pool)
            continue
        
        if guess not in valid_words:
            print("Not a valid word!")
            continue
        
        pattern, word_pool = get_best_outcome(guess, word_pool)
        
        if pattern == "22222":
            print(f"You won in {turns + 1} turns!")
            break
        
        print(f"Result: {pattern}")
        print(f"Remaining possibilities: {len(word_pool)}")
        
        turns += 1
    else:
        final_answer = random.choice(word_pool)
        print(f"\nGame over. You ran out of turns.")
        print(f"The word I 'totally' had in mind was: {final_answer}")
        

if __name__ == "__main__":
    main()