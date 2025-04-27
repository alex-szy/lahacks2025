from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"

if not CONFIG_DIR.exists():
    raise Exception(f"Config folder not found: {CONFIG_DIR}")

# Guaranteed to exist, else exception raised
WATCH_PATHS_FILE = CONFIG_DIR / "watch_paths.json"
if not WATCH_PATHS_FILE.exists():
    raise Exception(f"Watch paths file not found: {WATCH_PATHS_FILE}")

# Guaranteed to exist, else exception raised
FOLDER_PATHS_FILE = CONFIG_DIR / "folder_paths.json"
if not FOLDER_PATHS_FILE.exists():
    raise Exception(f"Folder paths file not found: {FOLDER_PATHS_FILE}")
