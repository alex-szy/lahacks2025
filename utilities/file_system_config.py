import json
from os import PathLike
from typing import Union
from ..settings import FOLDER_PATHS_FILE


class FileSystemConfig:
    def __init__(self, json_path: Union[str, bytes, PathLike] = FOLDER_PATHS_FILE):
        self.json_path = json_path
        print(json_path)

    def append_entry(self, path: str, description: str) -> None:
        data = json.loads(self.json_path.read_text())

        data.append({
            "file_path": path,
            "description": description
        })

        self.json_path.write_text(json.dumps(data, indent=2))

    def read_all_entries(self) -> dict[str, dict]:
        data = json.loads(self.json_path.read_text())
        result = {}
        for entry in data:
            result[entry["file_path"]] = {
                "description": entry["description"]
            }
        return result

    def read_entry(self, path: str) -> dict:
        all_entries = self.read_all_entries()
        return all_entries.get(path, {})
