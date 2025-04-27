# from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
# import os
import time

class VectorDatabase:
    def __init__(self, connection_string, db_name, collection_name, search_field):
        self.client = MongoClient(connection_string)
        self.db_name = db_name
        self.collection_name = collection_name
        self.search_field = search_field
    
    def save_search_index(self):
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": self.search_field,
                        "numDimensions": 1536,
                        "similarity": "cosine",
                        "quantization": "scalar"
                    }
                ]
            },
            name="vector_index",
            type="vectorSearch"
        )

        result = self.client[self.db_name][self.collection_name].create_search_index(model=search_index_model)
        print("New search index named " + result + " is building.")

        print("Polling to check if the index is ready. This may take up to a minute.")
        predicate=None
        if predicate is None:
            predicate = lambda index: index.get("queryable") is True

        while True:
            indices = list(self.client[self.db_name][self.collection_name].list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        print(result + " is ready for querying.")

    def get_query_results(self, query_embedding):
        pipeline = [
            {
                '$vectorSearch': {
                    'index': 'vector_index', 
                    'path': self.search_field, 
                    'queryVector': query_embedding, 
                    'numCandidates': 75, 
                    'limit': 5
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
        result = self.client[self.db_name][self.collection_name].aggregate(pipeline)
        return result

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
