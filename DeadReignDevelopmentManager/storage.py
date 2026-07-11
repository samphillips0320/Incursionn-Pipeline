import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"

ENTRIES_PATH = DATA_DIR / "development_entries.json"
SYSTEMS_PATH = DATA_DIR / "systems.json"

def ensure_data_directory():
    DATA_DIR.mkdir(exist_ok=True)

def load_json(file_path, default_value):
    ensure_data_directory()

    if not file_path.exists():
        return default_value

    if file_path.stat().st_size == 0:
        return default_value

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return default_value

def save_json(file_path, data):
    ensure_data_directory()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_systems():
    return load_json(SYSTEMS_PATH, [])

def save_new_system(system_name):
    systems = load_systems()

    if system_name not in systems:
        systems.append(system_name)
        systems.sort()
        save_json(SYSTEMS_PATH, systems)

def load_development_entries():
    return load_json(ENTRIES_PATH, [])

def save_development_entry(entry):
    entries = load_development_entries()
    entries.append(entry)
    save_json(ENTRIES_PATH, entries)

