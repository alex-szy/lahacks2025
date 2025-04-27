from __future__ import annotations
import os
from engine.encoder import Encoder
from db.database import VectorDatabase
from models.file import File
import datetime as dt
from typing import List, Dict, Set
from dotenv import load_dotenv


class QueryProcessor:
    def __init__(self, encoder: Encoder, db: VectorDatabase) -> None:
        self.encoder = encoder
        self.db = db

    def process_query(self, query: str, return_length: int = 5) -> List[File]:
        query_vec: List[float] = self.encoder.encode_query(
            query).tolist()        # now a plain list
        raw_rows: List[Dict] = self.db.get_query_results(query_vec)

        unique_rows: List[Dict] = self._deduplicate_rows(
            raw_rows, return_length)
        return self._build_files(unique_rows)

    def _deduplicate_rows(self, rows: List[Dict], limit: int) -> List[Dict]:
        """Drop duplicates (by file_path) and truncate to `limit` rows."""
        unique: List[Dict] = []
        seen: Set[str] = set()

        for row in rows:
            fp = row["file_path"]
            if fp in seen:
                continue
            seen.add(fp)
            unique.append(row)
            if len(unique) == limit:
                break
        return unique

    def _build_files(self, rows: List[Dict]) -> List[File]:
        """Turn DB rows into File objects enriched with metadata & summary."""
        files: List[File] = []

        for row in rows:
            fp: str = row["file_path"]
            summary: str = row.get("summary", "")

            try:
                stat = os.stat(fp)
                with open(fp, "rb") as fh:
                    content = fh.read()

                file_obj = File(
                    content=content,
                    name=os.path.basename(fp),
                    path=fp,
                    size_bytes=stat.st_size,
                    created_at=dt.datetime.fromtimestamp(
                        stat.st_ctime).isoformat(),
                    modified_at=dt.datetime.fromtimestamp(
                        stat.st_mtime).isoformat(),
                )
                file_obj.add_summary(summary)
                files.append(file_obj)

            except FileNotFoundError:
                # Skip missing files; replace with logging if desired
                continue

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
