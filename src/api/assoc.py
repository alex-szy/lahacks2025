from pathlib import Path

from settings import settings
from utils import is_forbidden


def add(folder_path: str, description: str):
    folder_path = str(Path(folder_path).resolve())
    if is_forbidden(folder_path):
        return False, f"'{folder_path}': Access is denied."
    paths = settings.get_folder_paths()
    paths[folder_path] = description
    settings.set_folder_paths(paths)
    return True, None


def remove(folder_path: str):
    folder_path = str(Path(folder_path).resolve())
    paths = settings.get_folder_paths()
    if folder_path in paths:
        del paths[folder_path]
        settings.set_folder_paths(paths)
        return True, None
    return (
        False,
        "The folder '{folder_path}' is not in the list of folder associations.",
    )


def list():
    return settings.get_folder_paths()
