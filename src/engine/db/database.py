import logging
import uuid

import chromadb
import chromadb.api
import chromadb.api.types

from engine.watcher import File
import engine.db.models as models


class VectorDatabase:
    def __init__(self):
        self.collection = chromadb.PersistentClient().get_or_create_collection(
            "munchkin_files"
        )

    """
    Stores embedding vector to db
    Input:
        embedding_vector: List
        file_path: str
    Output:
        None
    """

    def create_entry(self, file: File, summary: str):
        id = str(uuid.uuid4())
        self.collection.add(
            ids=id,
            documents=summary,
            metadatas={
                "path": file.path,
                "basename": file.basename,
                "extension": file.extension,
            },
        )
        logging.info(f"Created entry with id {id} for file {file.path}")

    def get_query_results(self, query: str, limit: int = 10):
        res = self.collection.query(
            query_texts=query, n_results=limit, include=["metadatas", "documents"]
        )

        return {
            id: models.File(
                summary=document,
                name=metadata["basename"],
                path=metadata["path"],
                extension=metadata["extension"],
            )
            for document, metadata, id in zip(
                res["documents"][0], res["metadatas"][0], res["ids"][0]
            )
        }

    def remove_entries(self, ids: chromadb.api.types.IDs):
        self.collection.delete(ids)
