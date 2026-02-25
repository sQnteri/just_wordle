import argparse
from src.engine import run_game
from src.config import GameSettings


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

   
def main():
    try:
        args = parse_args()
        settings = GameSettings(length=args.length, mode=args.mode, difficulty=args.difficulty, guesses=args.guesses)
        
        run_game(settings)
    except KeyboardInterrupt as e:
        print(e)
        try:
            exit(0)
        except SystemExit:
            pass
    
        

if __name__ == "__main__":
    main()