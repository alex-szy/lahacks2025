import os
import shutil
from typing import Optional

import numpy as np

from engine.classifier import Classifier
from engine.database import VectorDatabase
from engine.encoder import Encoder
from engine.database import File
from engine.preprocessor import Preprocessor

# from dotenv import load_dotenv


class SaveProcessor:
    def __init__(
        self,
        encoder: Encoder,
        classifier: Classifier,
        db: VectorDatabase,
        token_threshold: Optional[int] = None,
    ) -> None:
        self.encoder = encoder
        self.classifier = classifier
        self.db = db
        self.preprocessor = Preprocessor(token_threshold=token_threshold)

    def process_file(self, file_path: str) -> str:
        # 1. Read file from path
        file = self._load_file(file_path)

        # 2. Encode file content to embedding
        embedding: np.ndarray = self.encoder.encode_file(file)

        # 3. Classify file to determine target folder
        target_folder = self.classifier.classify(file)

        if target_folder:
            file_path = self._move_file(file.path, target_folder)

        # 5. Save embedding + new file path into database
        self.db.store_embedding_vector(embedding.tolist(), file_path, file.summary)

    def _load_file(self, file_path: str) -> File:
        with open(file_path, "rb") as f:
            content = f.read()
        filename = os.path.basename(file_path)
        return File(content=content, name=filename, path=file_path)

    def _move_file(self, original_path: str, target_folder: str) -> str:
        filename = os.path.basename(original_path)
        new_path = os.path.join(target_folder, filename)
        shutil.move(original_path, new_path)

        return new_path


# if __name__ == "__main__":
#     load_dotenv()
#     MONGO_URI = os.getenv("MONGO_URI")

#     db = VectorDatabase(MONGO_URI)
#     saveprocess = SaveProcessor(encoder=Encoder(), classifier=Classifier(), db=db)

#     saveprocess.process_and_save("path_to_file")
