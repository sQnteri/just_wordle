from pathlib import Path

def load_words(length):
    root_dir = Path(__file__).parent.parent
    filepath = root_dir / "data" / f"solutions_{length}.txt"
    
    if not filepath.exists():
        print(f"Error: File not found at {filepath}")
        return []
    
    try:
        with filepath.open(mode="r", encoding="utf-8-sig") as f:
            words = {line.strip().upper() for line in f if len(line.strip()) == length}
            return list(words)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def load_allowed_words():
    root_dir = Path(__file__).parent.parent
    filepath = root_dir / "data" / "allowed.txt"
    
    if not filepath.exists():
        print(f"Error: File not found at {filepath}")
        return set()
    
    try:
        with filepath.open(mode="r", encoding="utf-8-sig") as f:
            words = {line.strip().upper() for line in f}
            return words
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return set()
    
