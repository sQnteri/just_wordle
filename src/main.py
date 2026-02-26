import sys
from src.engine import run_game, settings_menu
from src.config import GameSettings
from src.ui import print_main_menu, print_settings_menu
from src import constants
from src.utils import clear_screen


def main():
    try:
        settings = GameSettings.load()
    except FileNotFoundError as e:
        print(f"\n[FATAL ERROR]: {e}")
        sys.exit(1)
    
    while True:
        print_main_menu(constants.MENU_WIDTH)
        choice = input(" > ").strip()
        
        if choice == '1':
            run_game(settings)
        elif choice == '2':
            settings_menu(settings)
        elif choice == '3':
            clear_screen()
            break
    
        

if __name__ == "__main__":
    main()