from sentence_transformers import SentenceTransformer
import faiss
from collections import defaultdict

from typing import List, Dict, Tuple
import numpy as np
from encoder.encoder import Encoder
from db.database import VectorDatabase
# from database import DB  # Assume your teammate will implement this

class QueryProcessor:
    def __init__(self, encoder: Encoder, db: VectorDatabase) -> None:
        self.encoder = encoder
        self.db = db  # DB object - treat as blackbox

    def process_query(self, query: str) -> List[str]:
        """
        1. Encode the natural language query to an embedding vector
        2. Send the query vector to the database
        3. Receive a list of relevant file paths
        """
        query_vector: np.ndarray = self.encoder.encode_query(query)
        file_paths: List[str] = [x['filepath'] for x in self.db.get_query_results(query_vector)]
        return file_paths

#OLD CODE

class SemanticIndexer:
    def __init__(self, model_name: str = "multi-qa-mpnet-base-dot-v1") -> None:
        self.model: SentenceTransformer = SentenceTransformer(model_name)
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: List[Dict[str, str]] = []
        self.search_counts: defaultdict[str, int] = defaultdict(int)

    def add_documents(self, docs: List[str], metadatas: List[Dict[str, str]]) -> None:
        all_passages = []
        all_passage_metadatas = []

        for doc_text, metadata in zip(docs, metadatas):
            passages = self.split_into_passages(doc_text, chunk_size=300)
            for idx, passage in enumerate(passages):
                all_passages.append(passage)
                passage_metadata = {
                    'filepath': metadata['filepath'],
                    'filename': metadata.get('filename', ''),
                    'chunk_index': idx,
                    'chunk_text': passage
                }
                all_passage_metadatas.append(passage_metadata)

        embeddings = self.model.encode(all_passages, normalize_embeddings=True)
        if self.index is None:
            dim = embeddings.shape[1]
            print(embeddings.shape)
            self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        self.metadata.extend(all_passage_metadatas)

    def encode_query(self, query: str) -> np.ndarray:
        return self.model.encode(query, normalize_embeddings=True)

    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, str], float]]:
        query_embedding: np.ndarray = self.encode_query(query)

        D, I = self.index.search(query_embedding.reshape(1, -1), k * 10)  # Over-retrieve more passages

        file_to_best: Dict[str, Tuple[Dict[str, str], float]] = {}

        for idx, semantic_score in zip(I[0], D[0]):
            if idx >= len(self.metadata):
                continue
            meta = self.metadata[idx]
            filepath = meta['filepath']
            filename = meta.get('filename', "")
            search_count = self.search_counts[filepath]

            hybrid_score = self.compute_hybrid_score(semantic_score, filename, query, search_count)

            # Keep only the best matching chunk per file
            if filepath not in file_to_best or hybrid_score > file_to_best[filepath][1]:
                file_to_best[filepath] = (meta, hybrid_score)

        # Convert dict values to list and sort by highest hybrid score
        results: List[Tuple[Dict[str, str], float]] = list(file_to_best.values())
        results.sort(key=lambda x: x[1], reverse=True)

        # Update search counts
        for meta, _ in results[:k]:
            self.search_counts[meta['filepath']] += 1

        return results[:k]

    @staticmethod
    def compute_hybrid_score(
        semantic_score: float,
        filename: str,
        query: str,
        search_count: int = 0,
        alpha: float = 0.7,
        beta: float = 0.2,
        gamma: float = 0.1
    ) -> float:
        keyword_match: int = int(any(word.lower() in filename.lower() for word in query.split()))
        popularity_score: float = np.log1p(search_count)  # log scaling
        hybrid_score: float = (alpha * semantic_score) + (beta * keyword_match) + (gamma * popularity_score)
        return hybrid_score

    @staticmethod
    def split_into_passages(text: str, chunk_size: int = 300) -> List[str]:
        words: List[str] = text.split()
        passages: List[str] = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            passages.append(chunk)
        return passages

    @staticmethod
    def format_result(meta: Dict[str, str], score: float) -> str:
        filename = meta.get('filename', 'Unknown File')
        filepath = meta.get('filepath', '')
        chunk_text = meta.get('chunk_text', 'No preview available')

        # Optionally truncate chunk text if too long
        preview = chunk_text[:400] + "..." if len(chunk_text) > 400 else chunk_text

        return (
            f"📄 **File:** {filename}\n"
            f"📂 **Path:** {filepath}\n"
            f"🔍 **Relevant Section:**\n\"{preview}\"\n"
            f"⭐ **Relevance Score:** {score:.4f}\n"
            "----------------------------------------"
        )

# ---------------- TEST SCRIPT ---------------- #

if __name__ == "__main__":
    indexer = SemanticIndexer()

    # Add some dummy documents
    documents = [
        "Lecture notes on Machine Learning, supervised and unsupervised models for dogs",
        "Homework assignment on ethics in Artificial Intelligence",
        "Research paper on applications of deep reinforcement learning in zoos.",
        "Summary of the AI conference discussing future of language models",
        "Email about the AI ethics group meeting next Friday",
        "HIHIHIHIIHHIHI",
        "nonoshirogsb alex albert hsus oa"

    ]

    metadata = [
        {'filepath': '/downloads/lecture_ml.txt', 'filename': 'lecture_ml.txt'},
        {'filepath': '/downloads/homework_ethics.txt', 'filename': 'homework_ethics.txt'},
        {'filepath': '/downloads/research_rl.txt', 'filename': 'research_rl.txt'},
        {'filepath': '/downloads/summary_ai_conference.txt', 'filename': 'summary_ai_conference.txt'},
        {'filepath': '/downloads/email_ethics_meeting.txt', 'filename': 'email_ethics_meeting.txt'}
    ]

    indexer.add_documents(documents, metadata)

    # Test a query
    query = "Find documents related to animals"

    results = indexer.search(query, k=3)

    # Pretty print results
    print("🔎 Top Search Results:")
    for meta, score in results:
        formatted = indexer.format_result(meta, score)
        print(formatted)
