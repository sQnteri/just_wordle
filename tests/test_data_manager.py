import pytest
from pathlib import Path
from src.data_manager import load_words

def test_load_words(tmp_path, monkeypatch):
    fake_project_root = tmp_path
    data_dir = fake_project_root / "data"
    data_dir.mkdir()
    
    word_file = data_dir / "solutions_5.txt"
    word_file.write_text("APPLE\n  BANANA  \ncAnDy", encoding="utf-8")
    
    fake_file_location = fake_project_root / "src" / "data_manager.py"
    monkeypatch.setattr("src.data_manager.Path", lambda *args: fake_file_location)
    
    
    words = load_words(5)
    assert "APPLE" in words
    assert "CANDY" in words
    assert "BANANA" not in words
    
def test_load_words_invalid_length(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    
    monkeypatch.setattr("src.data_manager.Path", lambda *args: tmp_path)
    assert load_words(99) == []
    