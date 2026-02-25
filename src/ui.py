from src.utils import clear_screen

# UI Constants
RESET = "\033[0m"
DIM   = "\033[2m"

# Keyboard Colors (Text only, Black background)
K_GREEN  = "\033[32m"
K_YELLOW = "\033[33m"
K_ABSENT = "\033[2;37m" # Dim + White/Gray text

# Board Colors (Background blocks with Black text)
B_GREEN  = "\033[30;42m" # Black text (30) on Green bg (42)
B_YELLOW = "\033[30;43m" # Black text (30) on Yellow bg (43)
B_GRAY   = "\033[30;47m" # Black text (30) on Gray bg (47)
B_EMPTY  = "\033[30;100m" # Black text on Dark Gray bg (for empty slots)

def print_main_menu(total_width):
    clear_screen()
    print("\n" * 2)
    print("=" * total_width)
    print("JUST WORDLE".center(total_width))
    print("=" * total_width)
    print("\n")
    print("1. PLAY GAME".center(total_width))
    print("2. SETTINGS".center(total_width))
    print("3. STATISTICS".center(total_width))
    print("4. EXIT".center(total_width))
    print("\n")
    print("=" * total_width)

def format_guess(guess, pattern):
    formatted_chars = []
    
    for i, char in enumerate(guess):
        p_val = pattern[i]
        
        if p_val == "2":
            color = B_GREEN
        elif p_val == "1":
            color = B_YELLOW
        else:
            color = B_GRAY
            
        formatted_chars.append(f"{color} {char} {RESET}")
    
    return " ".join(formatted_chars)

def print_header(settings, total_width):
    
    print("=" * total_width)
    
    print(f"JUST WORDLE: {settings.mode.upper()}".center(total_width))
    print(f"{settings.length} Letters | {settings.difficulty.upper()}".center(total_width))
    print("=" * total_width)
    print("(Type '!quit' to exit)".center(total_width))
    print("\n")
    
def print_board(guesses, settings, keyboard, status_msg):
    
    board_content_width = (settings.length * 3) + (settings.length - 1)
    total_width = board_content_width + 4 
    
    clear_screen()
    print_header(settings, total_width)
    
    for word, pattern in guesses:
        row = format_guess(word, pattern)
        print(f"\n  {row}{RESET}")
        
    remaining_attempts = settings.guesses - len(guesses)
    
    for _ in range(remaining_attempts):
        empty_slot = f"{B_GRAY}   {RESET}"
        empty_row = " ".join([empty_slot] * settings.length)
        print(f"\n  {empty_row}{RESET}")
    
    print("\n" + ("=" * total_width))
    print_keyboard(keyboard, total_width)
    if status_msg:
        print(f"{status_msg}{RESET}".center(total_width))
    
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
        print(f"✨ {K_GREEN} CONGRATULATIONS! {RESET} ✨")
        print(f"You found the word: {K_GREEN}{final_word}{RESET}")
    else:
        print(f"💀 {K_YELLOW} GAME OVER {RESET} 💀")
        print(f"The word was: {K_GREEN}{final_word}{RESET}")
        
def print_keyboard(keyboard, total_width):
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    print("\n" + "--- KEYBOARD ---".center(total_width))
    
    for i, row_str in enumerate(rows):
        formatted_letters = []
        for char in row_str:
            status = keyboard.get(char, 0)
            color = RESET
            if status == 3: color = K_GREEN
            elif status == 2: color = K_YELLOW
            elif status == 1: color = K_ABSENT
            
            formatted_letters.append(f"{color}{char}{RESET}")
        
        row_content = " ".join(formatted_letters)
        
        visible_width = (len(row_str) * 2) - 1
        
        padding = (total_width - visible_width) // 2
        
        print(" " * padding + row_content)
    
    print("=" * total_width)

    