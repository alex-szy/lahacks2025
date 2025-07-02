import os
import sys
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from models.file import File
from utilities.preprocessor import Preprocessor


class Encoder:
    def __init__(
        self,
        model_name: str = "multi-qa-mpnet-base-dot-v1",
        token_threshold: Optional[int] = 10000,
    ) -> None:
        self.model = SentenceTransformer(model_name)
        self.preprocessor = Preprocessor(token_threshold=token_threshold)

    def encode_query(self, query: str) -> np.ndarray:
        return self.model.encode(query, normalize_embeddings=True)

    def encode_file(self, file: File) -> np.ndarray:
        processed_text = self.preprocessor.preprocess(file)
        return self.model.encode(processed_text, normalize_embeddings=True)

    def get_embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
