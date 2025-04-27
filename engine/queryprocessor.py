from typing import List, Dict
import numpy as np
from engine.encoder import Encoder
from db.database import VectorDatabase

import os
from dotenv import load_dotenv


class QueryProcessor:
    def __init__(self, encoder: Encoder, db: VectorDatabase) -> None:
        self.encoder = encoder
        self.db = db

    def process_query(self, query: str, return_length=5) -> List[Dict]:
        """
        1. Encode the natural language query to an embedding vector
        2. Send the query vector to the database
        3. Receive a list of relevant file paths
        """
        query_vector: np.ndarray = self.encoder.encode_query(query).tolist()
        res = self.db.get_query_results(query_vector)
        file_paths = []
        seen = set()
        for r in res:
            file_path = r['file_path']
            if file_path in seen:
                continue
            seen.add(file_path)
            file_paths.append(r)
            if len(file_paths) >= return_length:
                break
        return file_paths

if __name__ == "__main__":
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    db = VectorDatabase(MONGO_URI)
    qp = QueryProcessor(Encoder(), db=db)
    
    query = "Search for my most played video game"
    res = qp.process_query(query)

    for r in res:
        print(r)
