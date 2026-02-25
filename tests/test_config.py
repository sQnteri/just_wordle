import pytest 
from pathlib import Path
from src.config import GameSettings

def test_scan_for_word_lists(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "solutions_5.txt").write_text("APPLE\nBEACH")
    (data_dir / "solutions_6.txt").write_text("APPLE\nBANANA")
    (data_dir / "allowed.txt").write_text("RANDM") # Should be ignored
    
    settings = GameSettings()
    
    lengths = []
    for file in data_dir.glob("solutions_*.txt"):
        try:
            num = int(file.stem.split("_")[1])
            lengths.append(num)
        except (ValueError, IndexError):
            continue
    assert sorted(lengths) == [5, 6]
        
    

