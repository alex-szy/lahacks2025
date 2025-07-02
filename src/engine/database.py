import logging
import time
from typing import Optional

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel


class VectorDatabase:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.db_name = "file_system"
        self.collection_name = "embedded_file"
        client = MongoClient(self.connection_string)
        logging.info("connected to database")
        client.close()

    """
    Stores embedding vector to db
    Input:
        embedding_vector: List
        file_path: str
    Output:
        None
    """

    def store_embedding_vector(self, embedding_vector, file_path, file_summary):
        client = MongoClient(self.connection_string)
        client[self.db_name][self.collection_name].insert_one(
            {
                "file_path": file_path,
                "file_embedding": embedding_vector,
                "file_summary": file_summary,
            }
        )
        client.close()

    """
    Performs cosine search and get closest query
    Input:
        query_embedding: List
        num_candidates: int
        limit: int
    Output:
        result: List[Dict] (descending order of similarity score, dict contains "file_path" key)
    """

    def get_query_results(self, query_embedding, num_candidates=20, limit=10):
        client = MongoClient(self.connection_string)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "file_embedding",
                    "queryVector": query_embedding,
                    "numCandidates": num_candidates,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "file_path": 1,
                    "file_summary": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]

        # run pipeline
        result = client[self.db_name][self.collection_name].aggregate(pipeline)
        client.close()
        return result

    def save_search_index(self, num_dimensions=768):
        client = MongoClient(self.connection_string)
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "file_embedding",
                        "numDimensions": num_dimensions,
                        "similarity": "cosine",
                        "quantization": "scalar",
                    }
                ]
            },
            name="vector_index",
            type="vectorSearch",
        )

        result = client[self.db_name][self.collection_name].create_search_index(
            model=search_index_model
        )
        logging.info("New search index named " + result + " is building.")

        logging.info(
            "Polling to check if the index is ready. This may take up to a minute."
        )
        predicate = None
        if predicate is None:

            def predicate(index):
                return index.get("queryable") is True

        while True:
            indices = list(
                client[self.db_name][self.collection_name].list_search_indexes(result)
            )
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        logging.info(result + " is ready for querying.")
        client.close()


class File:
    def __init__(
        self,
        content: bytes,
        name: str,
        summary: Optional[str] = None,
        extension: Optional[str] = None,
        path: Optional[str] = None,
        size_bytes: Optional[int] = None,
        created_at: Optional[str] = None,
        modified_at: Optional[str] = None,
    ):
        if not name:
            raise ValueError("File name must not be empty.")

        self.content = content
        self.name = name
        self.extension = extension or self._infer_extension()
        self.path = path
        self.size_bytes = size_bytes
        self.created_at = created_at
        self.modified_at = modified_at
        self.summary = summary

    def add_summary(self, summary: str) -> None:
        self.summary = summary

    def _infer_extension(self) -> Optional[str]:
        _, ext = os.path.splitext(self.name)
        return ext.lstrip(".") if ext else None

    def __repr__(self):
        return f"File(name={self.name}, summary={self.summary}, extension={self.extension})"
