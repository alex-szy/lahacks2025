from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import time

class VectorDatabase:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.db_name = "file_system"
        self.collection_name = "embedded_file"

    """
    Stores embedding vector to db
    Input:
        embedding_vector: List
        file_path: str
    Output:
        None
    """
    def store_embedding_vector(self, embedding_vector, file_path):
        client = MongoClient(self.connection_string)
        client[self.db_name][self.collection_name].insert_one({
            "file_path": file_path,
            "file_embedding": embedding_vector
        })
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
    def get_query_results(self, query_embedding, num_candidates=50, limit=15):
        client = MongoClient(self.connection_string)
        pipeline = [
            {
                '$vectorSearch': {
                    'index': "vector_index", 
                    'path': "file_embedding", 
                    'queryVector': query_embedding, 
                    'numCandidates': num_candidates, 
                    'limit': limit
                }
            },
            {
                '$project': {
                    '_id': 0, 
                    'file_path': 1,
                    'score': {
                        '$meta': 'vectorSearchScore'
                    }
                }
            }
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
                        "quantization": "scalar"
                    }
                ]
            },
            name="vector_index",
            type="vectorSearch"
        )

        result = client[self.db_name][self.collection_name].create_search_index(model=search_index_model)
        print("New search index named " + result + " is building.")

        print("Polling to check if the index is ready. This may take up to a minute.")
        predicate=None
        if predicate is None:
            predicate = lambda index: index.get("queryable") is True

        while True:
            indices = list(client[self.db_name][self.collection_name].list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        print(result + " is ready for querying.")
        client.close()

# def main():
#     try:
#         load_dotenv()
#         uri = os.getenv("MONGO_URI")
#         vector_db = VectorDatabase(uri, "file_system", "embedded_file", "file_embedding")
#         vector_db.save_search_index()
        
#         query_results = vector_db.get_query_results(query_embedding)

#         print("Printing query results...")
#         for q in query_results:
#             print(q)

#         # Close the connection
#         vector_db.client.close()
#         print("Client closed.")
        
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()
