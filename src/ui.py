import os
from src import constants


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_menu(total_width):
    clear_screen()
    print("\n" * 2)
    print("=" * total_width)
    print("JUST WORDLE".center(total_width))
    print("=" * total_width)
    print("\n")
    print("1. PLAY GAME".center(total_width))
    print("2. SETTINGS".center(total_width))
    print("3. EXIT".center(total_width))
    print("\n")
    print("=" * total_width)
    
def print_settings_menu(settings):
    clear_screen()
    print("=== JUST WORDLE SETTINGS ===")
    print("Use keys to toggle options\n")
    
    # 1. Lengths
    print(get_highlighted_row("(L) Word Length", settings.available_lengths, settings.length), "\n")
    
    # 2. Modes
    print(get_highlighted_row("(M) Mode", ["normal", "evil"], settings.mode), "\n")
    
    #3. Difficulty
    print(get_highlighted_row("(D) Diff", ["normal", "hard"], settings.difficulty), "\n")
    
    #4. Guesses
    available_guesses_visual = ["inf" if x == 0 else x for x in settings.available_guesses]
    guesses_visual = "inf" if settings.guesses == 0 else settings.guesses
    print(get_highlighted_row("(G) Max Guesses", available_guesses_visual, guesses_visual), "\n")
    
    print("\n" + "-" * 30)
    print("(R) Restore defaults\n(S) Save and quit: Save changes permanently\n(Q) Quit: Save settings only for current session")
    
def get_highlighted_row(label, options, current_value):
    """
    Example: Word Length: [ 5 ] [ 6 ] [ 7 ]
    (if 5 is active, [ 5 ] will be green)
    """
    row_str = f"{label:16}: "
    for opt in options:
        if str(opt).lower() == str(current_value).lower():
            row_str += f"{constants.K_GREEN} [ {opt} ] {constants.RESET} "
        else:
            row_str += f"  {opt}   "
    return row_str

def format_guess(guess, pattern):
    formatted_chars = []
    
    for i, char in enumerate(guess):
        p_val = pattern[i]
        
        if p_val == "2":
            color = constants.B_GREEN
        elif p_val == "1":
            color = constants.B_YELLOW
        else:
            color = constants.B_WRONG
            
        formatted_chars.append(f"{color} {char} {constants.RESET}")
    
    return " ".join(formatted_chars)

def print_header(settings, total_width):
    
    print("=" * total_width)
    
    print(f"JUST WORDLE: {settings.mode.upper()}".center(total_width))
    print(f"{settings.length} Letters | {settings.difficulty.upper()}".center(total_width))
    print("=" * total_width)
    print("(Type 'q' to exit)".center(total_width))
    print("\n")
    
def print_board(guesses, settings, keyboard, status_msg):
    
    board_content_width = (settings.length * 3) + (settings.length - 1)
    total_width = board_content_width + 4 
    
    clear_screen()
    print_header(settings, total_width)
    
    for word, pattern in guesses:
        row = format_guess(word, pattern)
        print(f"\n  {row}{constants.RESET}")
    
    total_guesses = float("inf") if settings.guesses == 0 else settings.guesses
    
    remaining_attempts = 0
    
    # 0 represents infinite mode
    if settings.guesses != 0:
        remaining_attempts = total_guesses - len(guesses)
    
    # number of static lines + 2 lines per guess (newlines between them)
    if (15 + (2 * total_guesses) <= os.get_terminal_size().lines):
         print_empty_rows(settings, remaining_attempts)
    
    
    
    print("\n" + ("=" * total_width))
    print_keyboard(keyboard, total_width)
    if status_msg:
        print(f"{status_msg}{constants.RESET}".center(total_width))

def print_empty_rows(settings, remaining_attempts):
    for _ in range(remaining_attempts):
        empty_slot = f"{constants.B_GRAY}   {constants.RESET}"
        empty_row = " ".join([empty_slot] * settings.length)
        print(f"\n  {empty_row}{constants.RESET}")
    
def print_result(won, secret_word, word_pool, guesses, settings, keyboard, status_message):
    # 1. Final UI Refresh
    print_board(guesses, settings, keyboard, status_message)
    
    # 2. Resolve the "Actual" Word
    if settings.mode == "evil":
        if won:
            # If they won, the word is their last guess
            final_word = guesses[-1][0]
        else:
            # If they lost, pick a random survivor from the pool
            import random
            final_word = random.choice(word_pool)
    else:
        # Normal mode already has a secret_word
        final_word = secret_word

    # 3. Display Messages
    if won:
        print(f"✨ {constants.K_GREEN} CONGRATULATIONS! {constants.RESET} ✨")
        print(f"You found the word: {constants.K_GREEN}{final_word}{constants.RESET}")
    else:
        print(f"💀 {constants.K_YELLOW} GAME OVER {constants.RESET} 💀")
        print(f"The word was: {constants.K_GREEN}{final_word}{constants.RESET}")
    input("Press Enter to go back to main menu")
        
def print_keyboard(keyboard, total_width):
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    print("\n" + "--- KEYBOARD ---".center(total_width))
    
    for i, row_str in enumerate(rows):
        formatted_letters = []
        for char in row_str:
            status = keyboard.get(char, 0)
            color = constants.RESET
            if status == 3: color = constants.K_GREEN
            elif status == 2: color = constants.K_YELLOW
            elif status == 1: color = constants.K_ABSENT
            
            formatted_letters.append(f"{color}{char}{constants.RESET}")
        
        row_content = " ".join(formatted_letters)
        
        visible_width = (len(row_str) * 2) - 1
        
        padding = (total_width - visible_width) // 2
        
        print(" " * padding + row_content)
    
    print("=" * total_width)

    