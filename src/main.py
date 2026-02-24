import sys
import argparse
from dataclasses import dataclass
from data_manager import load_words
from logic import match_pattern, get_evil_outcome, is_hard_mode_compliant, get_updated_keyboard
from utils import clear_screen
from ui import print_board, print_result


def parse_args():
    parser = argparse.ArgumentParser(description="Evil Wordle")
    
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=5,
        choices=[5, 6, 7],
        help="Number of letters in the word (default: 5)"
    )
    
    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="normal",
        choices=["normal", "evil", "impossible"],
        help="Game difficulty (default: normal)"
    )
    
    parser.add_argument(
        "-d", "--difficulty",
        type=str,
        default="normal",
        choices=["normal", "hard"],
        help="Game rules (default: normal)"
    )
    
    parser.add_argument(
        "-g", "--guesses",
        type=int,
        default=6,
        choices=[i for i in range(1, 100)],
        help="Number of guesses 1-100 (default: 6)"
    )
    
    return parser.parse_args()

@dataclass
class GameSettings:
    length: int
    mode: str
    difficulty: int
    guesses: int
    

def run_game(settings):
    
    word_pool = load_words(settings.length)
    if not word_pool:
        print("Could not load words. Check your data folder.")
        return
    
    secret_word = None
    if settings.mode == "normal":
        import random
        secret_word = random.choice(word_pool)
        
    guesses = []
    won = False
    max_turns = settings.guesses
    keyboard = {l: 0 for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    status_msg = "" # To hold error messages between refreshes
    
    while len(guesses) < max_turns:
        print_board(guesses, settings, keyboard, status_msg)
        status_msg = "" # Reset message after displaying
        
        turn_num = len(guesses) + 1
        guess = input(f"Guess {turn_num}/{max_turns}: ").strip().upper()
        
        if guess == "!QUIT":
            print("Quitting game...")
            return

        if len(guess) != settings.length:
            status_msg = f"Error: Guess must be {settings.length} letters."
            continue
        
        if settings.difficulty == "hard" and guesses:
            last_guess, last_pattern = guesses[-1]
            is_valid, error_list = is_hard_mode_compliant(guess, last_guess, last_pattern)
           
            if not is_valid:
                status_msg = "Hard Mode Rules:\n   • " + "\n   • ".join(error_list)
                continue
    
        if settings.mode == "evil":
            pattern, word_pool = get_evil_outcome(guess, word_pool)
        else:
            pattern = match_pattern(guess, secret_word)
        
        keyboard = get_updated_keyboard(keyboard, guess, pattern)
        guesses.append((guess, pattern))
    
        if pattern == "2" * settings.length:
            won = True
            break
    
    print_result(won, secret_word, word_pool, guesses, settings)
    
    
def main():
    try:
        args = parse_args()
        settings = GameSettings(length=args.length, mode=args.mode, difficulty=args.difficulty, guesses=args.guesses)
        
        word_pool = load_words(settings.length)
        
        if not word_pool:
            print("Empty word pool. Exiting.")
            sys.exit(1)
        
        run_game(settings)
    except KeyboardInterrupt as e:
        print(e)
        try:
            exit(0)
        except SystemExit:
            pass
    
        

if __name__ == "__main__":
    main()