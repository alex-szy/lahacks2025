from typing import List, Dict
from encoder import SemanticIndexer

def build_index(documents: List[str], metadatas: List[Dict[str, str]]) -> SemanticIndexer:
    indexer = SemanticIndexer()
    indexer.add_documents(documents, metadatas)
    return indexer

def run_query(indexer: SemanticIndexer, query: str, top_k: int = 5) -> None:
    results = indexer.search(query, k=top_k)
    print("🔎 Top Search Results:")
    for meta, score in results:
        formatted = indexer.format_result(meta, score)
        print(formatted)

if __name__ == "__main__":
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

    indexer = build_index(documents, metadata)
    
    query = "Find documents related to animals"
    run_query(indexer, query, top_k=3)
