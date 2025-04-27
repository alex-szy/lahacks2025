from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import os
import time

def connect_to_atlas(connection_string):
    client = MongoClient(connection_string)
    print("Connected to client.")
    return client

def get_collection(client, db_name, collection_name):
    database = client[db_name]
    collection = database[collection_name]
    return collection

def get_query_results(client, query_embedding, search_field):
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector_index', 
                'path': search_field, 
                'queryVector': query_embedding, 
                'numCandidates': 75, 
                'limit': 5
            }
        },
        {
            '$project': {
                '_id': 0, 
                'folder_path': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]

    # run pipeline
    result = client["file_system"]["embedded_file"].aggregate(pipeline)
    return result

def main():
    try:
        load_dotenv()
        uri = os.getenv("MONGO_URI")

        client = connect_to_atlas(uri)
        collection = get_collection(client, "file_system", "embedded_file")

        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "file_embedding",
                        "numDimensions": 1536,
                        "similarity": "cosine",
                        "quantization": "scalar"
                    }
                ]
            },
            name="vector_index",
            type="vectorSearch"
        )

        result = collection.create_search_index(model=search_index_model)
        print("New search index named " + result + " is building.")

        print("Polling to check if the index is ready. This may take up to a minute.")
        predicate=None
        if predicate is None:
            predicate = lambda index: index.get("queryable") is True

        while True:
            indices = list(collection.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)
        print(result + " is ready for querying.")
        
        query_results = get_query_results(client, query_embedding, "file_embedding")

        print("Printing query results...")
        for q in query_results:
            print(q)

        # Close the connection
        client.close()
        print("Client closed.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
