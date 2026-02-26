import os
import json
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path

@dataclass
class GameSettings:
    length: int = 5
    mode: str = "normal"
    difficulty: str = "normal"
    guesses: int = 6
    available_lengths: list[int] = field(default_factory=list)
    available_guesses: list[int] = field(default_factory=list)
    
    def __post_init__(self):
        self.available_lengths = self._scan_for_word_lists()
        if self.length not in self.available_lengths:
            if self.available_lengths:
                self.length = self.available_lengths[0]
            else:
                raise FileNotFoundError("No word lists (solutions_*.txt) found in data/ directory.")
        self.available_guesses = [i for i in range(13)]
    
    def _scan_for_word_lists(self):
        """Looks for solutions_N.txt files in the data folder relative to project root"""
        root_dir = Path(__file__).parent.parent
        data_path = root_dir / "data"
        
        lengths = []
        if data_path.exists():
            for file in data_path.glob("solutions_*.txt"):
                try:
                    # solutions_N.txt -> stem is 'solutions_N' -> split gives 'N'
                    num = int(file.stem.split("_")[1])
                    lengths.append(num)
                except (ValueError, IndexError):
                    continue
        return sorted(lengths)
    
    def restore_defaults(self):
        default = GameSettings()
        for field in fields(self):
            setattr(self, field.name, getattr(default, field.name))
    
    def toggle_length(self):
        lengths = self.available_lengths
        current_idx = lengths.index(self.length)
        self.length = lengths[(current_idx + 1) % len(lengths)]
        
    def toggle_guesses(self):
        guesses = self.available_guesses
        current_idx = guesses.index(self.guesses)
        self.guesses = guesses[(current_idx + 1) % len(guesses)]
        
    def toggle_mode(self):
        self.mode = "evil" if self.mode == "normal" else "normal"
        
    def toggle_difficulty(self):
        self.difficulty = "hard" if self.difficulty == "normal" else "normal"
        
    def save(self):
        with open("settings.json", "w") as f:
            data = asdict(self)
            data.pop("available_lengths", None)
            data.pop("available_guesses", None)
            json.dump(data, f, indent=4)
            
    @classmethod
    def load(cls):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    data = json.load(f)
                    return cls(**data)
            except Exception as e:
                return cls()  # Fallback to defaults
        return cls()
                
                    
        
            
        