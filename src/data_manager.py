import os

def load_words(length):
    filename = f"data/solutions_{length}.txt"
    # 1. Path to: /.../just_wordle/src/data_manager.py
    this_file_path = os.path.abspath(__file__)
    # 2. Path to: /.../just_wordle/src/
    src_dir = os.path.dirname(this_file_path)
    # 3. Path to: /.../just_wordle/
    root_dir = os.path.dirname(src_dir)
    # 4. Final Path to: /.../just_wordle/data/solutions_X.txt
    filepath = os.path.join(root_dir, 'data', f"solutions_{length}.txt")
    
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return []
    
    try:
        with open(filepath, "r") as f:
            words = [line.strip().upper() for line in f if line.strip()]
            return words
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
