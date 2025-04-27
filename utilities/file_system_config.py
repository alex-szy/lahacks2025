import json
from os import PathLike
import os
from typing import Union
from settings import FOLDER_PATHS_FILE


class FileSystemConfig:
    def __init__(self, json_path: Union[str, bytes, PathLike] = FOLDER_PATHS_FILE):
        self.json_path = json_path

    def append_entry(self, path: str, description: str) -> None:
        data = json.load(open(self.json_path))

        data.append({
            "file_path": path,
            "description": description
        })

        json.dump(data, open(self.json_path, "w"), indent=2)

    def remove_entry(self, path: str) -> None:
        data = json.load(open(self.json_path))

        data = [entry for entry in data if os.path.normpath(
            entry.get("file_path")) != path]

        json.dump(data, open(self.json_path, "w"), indent=2)

    def read_all_entries(self) -> dict[str, dict]:
        data = json.load(open(self.json_path))
        result = {}
        for entry in data:
            result[entry["file_path"]] = {
                "description": entry["description"]
            }
        return result

    def read_entry(self, path: str) -> dict:
        all_entries = self.read_all_entries()
        return all_entries.get(path, {})
