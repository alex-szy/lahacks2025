from __future__ import annotations

import datetime as dt
from pathlib import Path


from engine.db.database import VectorDatabase
from engine.db.models import File


class QueryProcessor:
    def __init__(self, db: VectorDatabase) -> None:
        self.db = db

    def process_query(self, query: str, return_length: int = 5) -> list[File]:
        files = self.db.get_query_results(query, return_length)
        res = []
        seen = set()
        cleanup = []
        for id, file in files.items():
            path = Path(file.path).resolve()
            if path in seen:
                cleanup.append(id)
                continue
            try:
                stat = path.stat()
                file.size_bytes = stat.st_size
                file.created_at = dt.datetime.fromtimestamp(stat.st_ctime).isoformat()
                file.modified_at = dt.datetime.fromtimestamp(stat.st_mtime).isoformat()
                seen.add(path)
                res.append(file)
            except (FileNotFoundError, PermissionError, OSError):
                cleanup.append(id)

        self.db.remove_entries(cleanup)

        return res
