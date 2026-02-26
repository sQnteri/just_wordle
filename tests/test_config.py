import pytest 
from pathlib import Path
from src.config import GameSettings

def test_scan_for_word_lists(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "solutions_5.txt").write_text("APPLE\nBEACH")
    (data_dir / "solutions_6.txt").write_text("APPLE\nBANANA")
    
    def mock_scan(self):
        lengths = []
        for file in data_dir.glob("solutions_*.txt"):
            lengths.append(int(file.stem.split("_")[1]))
        return sorted(lengths)

    monkeypatch.setattr(GameSettings, "_scan_for_word_lists", mock_scan)
    
    settings = GameSettings()
    assert settings.available_lengths == [5, 6]
        
    

