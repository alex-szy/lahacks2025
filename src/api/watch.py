from pathlib import Path

from api.daemon import refresh_if_running
from settings import settings
from utils import is_forbidden


def add(folder_path: str):
    resolved_path = Path(folder_path).expanduser().resolve()

    folder_path = str(resolved_path)
    if not resolved_path.is_dir():
        return False, f"The path '{folder_path}' is not a directory."

    if is_forbidden(folder_path):
        return False, f"'{folder_path}': Access is denied."

    paths = settings.get_watch_paths()
    if folder_path in paths:
        return False, f"The folder '{folder_path}' is already being watched."

    paths.append(folder_path)
    settings.set_watch_paths(paths)
    refresh_if_running()
    return True, None


def remove(folder_path: str):
    folder_path = str(Path(folder_path).expanduser().resolve())

    paths = settings.get_watch_paths()
    if folder_path not in paths:
        return False, f"The folder '{folder_path}' is not in the watch list."

    paths.remove(folder_path)
    settings.set_watch_paths(paths)
    refresh_if_running()
    return True, None


def list():
    return settings.get_watch_paths()
