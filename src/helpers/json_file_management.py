import os
import json


class JsonFileManager:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def save(self, data: dict):
        """Save the given dict to the JSON file."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> dict:
        """Load and return the contents of the JSON file."""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"JSON file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update(self, updates: dict):
        """Update existing JSON file with provided key-value pairs."""
        data = self.load()
        data.update(updates)
        self.save(data)
