from utils import clear_screen

# ANSI Background Colors
GREEN = '\033[42m\033[30m'  # Black text on Green bg
YELLOW = '\033[43m\033[30m' # Black text on Yellow bg
GRAY = '\033[100m\033[37m'  # White text on Gray bg
RESET = '\033[0m'           # Back to normal

def format_guess(guess, pattern):
    formatted_chars = []
    
    for i, char in enumerate(guess):
        p_val = pattern[i]
        
        if p_val == "2":
            color = GREEN
        elif p_val == "1":
            color = YELLOW
        else:
            color = GRAY
            
        formatted_chars.append(f"{color} {char} {RESET}")
    
    return " ".join(formatted_chars)

def print_header(settings, total_width):
    
    print("=" * total_width)
    
    print(f"JUST WORDLE: {settings.mode.upper()}".center(total_width))
    print(f"{settings.length} Letters | {settings.difficulty.upper()}".center(total_width))
    print("=" * total_width)
    print("(Type 'QUIT' to exit)".center(total_width))
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
        empty_slot = f"{GRAY}   {RESET}"
        empty_row = " ".join([empty_slot] * settings.length)
        print(f"\n  {empty_row}{RESET}")
    
    print("\n" + ("=" * total_width))
    print_keyboard(keyboard, total_width)
    if status_msg:
        print(f"{status_msg}{RESET}".center(total_width))
    
def print_result(won, secret_word, word_pool, guesses, settings):
    # 1. Final UI Refresh
    print_board(guesses, settings)
    
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
        print(f"✨ {GREEN} CONGRATULATIONS! {RESET} ✨")
        print(f"You found the word: {GREEN}{final_word}{RESET}")
    else:
        print(f"💀 {GRAY} GAME OVER {RESET} 💀")
        print(f"The word was: {GREEN}{final_word}{RESET}")
        
def print_keyboard(keyboard, total_width):
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    print("\n" + "--- KEYBOARD ---".center(total_width))
    
    for i, row_str in enumerate(rows):
        formatted_letters = []
        for char in row_str:
            status = keyboard.get(char, 0)
            color = RESET
            if status == 3: color = GREEN
            elif status == 2: color = YELLOW
            elif status == 1: color = GRAY
            
            formatted_letters.append(f"{color}{char}{RESET}")
        
        row_content = " ".join(formatted_letters)
        
        visible_width = (len(row_str) * 2) - 1
        
        padding = (total_width - visible_width) // 2
        
        print(" " * padding + row_content)
    
    print("=" * total_width)

    