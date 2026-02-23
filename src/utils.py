import argparse

def load_words(filepath):
    with open(filepath, 'r') as f:
        return [line.strip().upper() for line in f if len(line.strip()) == 5]
    
def parse_args():
    parser = argparse.ArgumentParser(description="The Evil Worldle Engine")
    parser.add_argument(
        "-m", "--mode",
        choices=["easy", "normal", "impossible"],
        help="Set the game difficulty"
    )
    return parser.parse_args()