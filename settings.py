import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
ASSETS_DIR = BASE_DIR / "assets"

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

DOTENV_PATH = BASE_DIR / ".env"

if not DOTENV_PATH.exists():
    raise FileNotFoundError(f"Missing .env file at {DOTENV_PATH}")

load_dotenv(dotenv_path=DOTENV_PATH)

# Guaranteed to exist, else exception raised
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in .env")
