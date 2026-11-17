from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "config.json"
)
try:
    with open(CONFIG_PATH, "r", encoding= "utf-8") as f:
        config_data = json.load(f)
except FileNotFoundError:
    print("Error: File Not found")
except json.JSONDecodeError:
    print("Error: Json Decode Error")


