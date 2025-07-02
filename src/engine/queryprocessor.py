from __future__ import annotations

import datetime as dt
import os
from typing import Dict, List, Set

from dotenv import load_dotenv

from engine.database import VectorDatabase
from engine.encoder import Encoder
from engine.database import File


class QueryProcessor:
    def __init__(self, encoder: Encoder, db: VectorDatabase) -> None:
        self.encoder = encoder
        self.db = db

    def process_query(self, query: str, return_length: int = 5) -> List[File]:
        query_vec: List[float] = self.encoder.encode_query(
            query
        ).tolist()  # now a plain list
        raw_rows: List[Dict] = self.db.get_query_results(query_vec)

        unique: List[Dict] = []
        seen: Set[str] = set()

        for row in raw_rows:
            fp = row["file_path"]
            if fp in seen:
                continue
            seen.add(fp)
            unique.append(row)

        return self._build_files(unique)

    def _build_files(self, rows: List[Dict]) -> List[File]:
        """Turn DB rows into File objects enriched with metadata & summary."""
        files: List[File] = []

        for row in rows:
            fp: str = row["file_path"]
            summary: str = row.get("file_summary", "")

            try:
                stat = os.stat(fp)

                file_obj = File(
                    content="",
                    name=os.path.basename(fp),
                    path=fp,
                    summary=summary,
                    size_bytes=stat.st_size,
                    created_at=dt.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    modified_at=dt.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                )
                files.append(file_obj)

            except FileNotFoundError:
                # Skip missing files; replace with logging if desired
                file_obj = File(
                    content="",
                    summary=summary,
                    name=fp,
                )
                files.append(file_obj)

        return files


if __name__ == "__main__":
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    db = VectorDatabase(MONGO_URI)
    qp = QueryProcessor(Encoder(), db=db)

    query = "Search for my most played video game"
    res = qp.process_query(query)

    for r in res:
        print(r)
