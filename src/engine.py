from src.logic import match_pattern, get_evil_outcome, is_hard_mode_compliant, get_updated_keyboard
from src.ui import print_board, print_result, print_settings_menu
from src.data_manager import load_words, load_allowed_words

def settings_menu(settings):
    while True:
        print_settings_menu(settings)
        
        choice = input("\nSelect an option: ").strip().upper()
        
        if choice == 'L':
            settings.toggle_length()
        elif choice == 'M':
            settings.toggle_mode()
        elif choice == 'D':
            settings.toggle_difficulty()
        elif choice == 'G':
            settings.toggle_guesses()
        elif choice == 'R':
            settings.restore_defaults()
        elif choice == 'S':
            settings.save()
            return
        elif choice == 'Q':
            return
            

def run_game(settings):
    
    word_pool = load_words(settings.length)
    allowed_words = load_allowed_words()
    
    if not word_pool or not allowed_words:
        print("Could not load words. Check your data folder.")
        return
    
    secret_word = None
    if settings.mode == "normal":
        import random
        secret_word = random.choice(word_pool)
        
    guesses = []
    won = False
    max_turns = float("inf") if settings.guesses == 0 else settings.guesses
    keyboard = {l: 0 for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    status_msg = "" # To hold error messages between refreshes
    
    while len(guesses) < max_turns:
        print_board(guesses, settings, keyboard, status_msg)
        status_msg = "" # Reset message after displaying
        
        turn_num = len(guesses) + 1
        
        input_prompt = f"Guess {turn_num}: " if max_turns == float("inf") else f"Guess {turn_num}/{max_turns}: "
        guess = input(input_prompt).strip().upper()
        
        if guess == "Q":
            return

        if len(guess) != settings.length:
            status_msg = f"Error: Guess must be {settings.length} letters."
            continue
        
        if guess in [g for g, p in guesses]:
            status_msg = f"Error: You already guessed this word."
            continue
        
        if guess not in allowed_words:
            status_msg = f"Error: Guess must be a valid english word."
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
    
    print_result(won, secret_word, word_pool, guesses, settings, keyboard, status_msg)
    
