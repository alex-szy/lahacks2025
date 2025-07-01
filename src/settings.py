import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
ASSETS_DIR = BASE_DIR / "assets"
MONGO_URI = None


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(object, metaclass=Singleton):
    def __init__(self):
        self.__config = {}
        self.__pull()

    def get_gemini_api_key(self):
        self.__pull()
        return self.__config.get("gemini_api_key")

    def set_gemini_api_key(self, key: str):
        self.__config["gemini_api_key"] = key
        self.__push()

    def get_watch_paths(self) -> List[str]:
        self.__pull()
        return self.__config.get("watch_paths", [])

    def set_watch_paths(self, paths: List[str]):
        self.__config["watch_paths"] = paths
        self.__push()

    def get_folder_paths(self) -> Dict[str, str]:
        self.__pull()
        return self.__config.get("folder_paths", {})

    def set_folder_paths(self, paths: Dict[str, str]):
        self.__config["folder_paths"] = paths
        self.__push()

    def __push(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.__config, f, indent=4)

    def __pull(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                self.__config = json.load(f)
        except (FileNotFoundError, JSONDecodeError) as e:
            logging.error(f"Error loading config file at {CONFIG_FILE}: {e}")
            self.__config = {}


settings = Settings()
if settings.get_gemini_api_key() is None:
    settings.set_gemini_api_key(input("Please enter the gemini api key: "))
