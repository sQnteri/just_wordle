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
B_WRONG = "\033[38;5;0;48;5;250m"

MENU_WIDTH = 50