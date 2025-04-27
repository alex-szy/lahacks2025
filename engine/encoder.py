from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple

class SemanticIndexer:
    def __init__(self, model_name: str = "multi-qa-mpnet-base-dot-v1") -> None:
        self.model: SentenceTransformer = SentenceTransformer(model_name)
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: List[Dict[str, str]] = []
        self.search_counts: defaultdict[str, int] = defaultdict(int)

    # def add_documents(self, docs: List[str], metadatas: List[Dict[str, str]]) -> None:
    #     embeddings: np.ndarray = self.model.encode(docs, normalize_embeddings=True)
    #     if self.index is None:
    #         dim: int = embeddings.shape[1]
    #         self.index = faiss.IndexFlatIP(dim)
    #     self.index.add(embeddings)
    #     self.metadata.extend(metadatas)

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
            self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        self.metadata.extend(all_passage_metadatas)


    def encode_query(self, query: str) -> np.ndarray:
        return self.model.encode(query, normalize_embeddings=True)

    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, str], float]]:
        query_embedding: np.ndarray = self.encode_query(query)

        D, I = self.index.search(query_embedding.reshape(1, -1), k * 5)  # Over-retrieve for reranking

        candidates: List[Tuple[Dict[str, str], float]] = []
        for idx, semantic_score in zip(I[0], D[0]):
            if idx >= len(self.metadata):  # Safety check
                continue
            meta = self.metadata[idx]
            filepath = meta['filepath']
            filename = meta.get('filename', "")
            search_count = self.search_counts[filepath]

            hybrid_score: float = self.compute_hybrid_score(semantic_score, filename, query, search_count)
            candidates.append((meta, hybrid_score))

        candidates.sort(key=lambda x: x[1], reverse=True)

        for meta, _ in candidates[:k]:
            self.search_counts[meta['filepath']] += 1

        return candidates[:k]
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, str], float]]:
        query_embedding: np.ndarray = self.encode_query(query)

        D, I = self.index.search(query_embedding.reshape(1, -1), k * 5)

        candidates: List[Tuple[Dict[str, str], float]] = []
        for idx, semantic_score in zip(I[0], D[0]):
            if idx >= len(self.metadata):
                continue
            meta = self.metadata[idx]
            filepath = meta['filepath']
            filename = meta.get('filename', "")
            chunk_text = meta.get('chunk_text', "")
            search_count = self.search_counts[filepath]

            hybrid_score = self.compute_hybrid_score(semantic_score, filename, query, search_count)
            candidates.append((meta, hybrid_score))

        candidates.sort(key=lambda x: x[1], reverse=True)

        for meta, _ in candidates[:k]:
            self.search_counts[meta['filepath']] += 1

        return candidates[:k]


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

    
indexer = SemanticIndexer()

# 2. Add some dummy documents
documents = [
    "Lecture notes on Machine Learning, supervised and unsupervised models for dogs",
    "Homework assignment on ethics in Artificial Intelligence",
    "Research paper on applications of deep reinforcement learning in zoos.",
    "Summary of the AI conference discussing future of language models",
    "Email about the AI ethics group meeting next Friday"
]

metadata = [
    {'filepath': '/downloads/lecture_ml.txt', 'filename': 'lecture_ml.txt'},
    {'filepath': '/downloads/homework_ethics.txt', 'filename': 'homework_ethics.txt'},
    {'filepath': '/downloads/research_rl.txt', 'filename': 'research_rl.txt'},
    {'filepath': '/downloads/summary_ai_conference.txt', 'filename': 'summary_ai_conference.txt'},
    {'filepath': '/downloads/email_ethics_meeting.txt', 'filename': 'email_ethics_meeting.txt'}
]

indexer.add_documents(documents, metadata)

# 3. Test a query
query = "Find documents related to animals"

results = indexer.search(query, k=3)

# 4. Print results
print("Top search results:")
for meta, score in results:
    print(f"File: {meta['filename']} | Score: {score:.4f} | Path: {meta['filepath']}")

