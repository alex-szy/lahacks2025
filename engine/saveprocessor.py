import os
import shutil
import numpy as np
from typing import Optional
from engine.encoder import Encoder

import os
from dotenv import load_dotenv
from pymongo import MongoClient

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import VectorDatabase
from models.file import File
from utilities.preprocessor import Preprocessor
from classifier.classifier import Classifier


class SaveProcessor:
    def __init__(self, encoder: Encoder, classifier: Classifier, db: VectorDatabase, token_threshold: Optional[int] = None) -> None:
        self.encoder = encoder
        self.classifier = classifier
        self.db = db
        self.preprocessor = Preprocessor(token_threshold=token_threshold)

    def process_and_save(self, file_path: str) -> None:
        # 1. Read file from path
        file = self._load_file(file_path)

        # 2. Encode file content to embedding
        embedding: np.ndarray = self.encoder.encode_file(file)

        # 3. Classify file to determine target folder
        target_folder: str = self.classifier.classify(file)

        # 4. Move file to target folder
        new_file_path = self._move_file(file.path, target_folder)

        # 5. Save embedding + new file path into database
        self.db.store_embedding_vector(embedding.tolist(), new_file_path)

    def _load_file(self, file_path: str) -> File:
        with open(file_path, "rb") as f:
            content = f.read()
        filename = os.path.basename(file_path)
        return File(content=content, name=filename, path=file_path)

    def _move_file(self, original_path: str, target_folder: str) -> str:
        os.makedirs(target_folder, exist_ok=True)
        filename = os.path.basename(original_path)
        new_path = os.path.join(target_folder, filename)
        # shutil.move(original_path, new_path)
        print(new_path)
        return new_path

if __name__ == "__main__":
# Load the .env file
    load_dotenv()

    # Fetch values
    MONGO_URI = os.getenv("MONGO_URI")
    print(MONGO_URI)
    db = VectorDatabase(MONGO_URI)
    saveprocess = SaveProcessor(encoder=Encoder(), classifier=Classifier(), db=db)
    saveprocess.process_and_save("experiment.txt")