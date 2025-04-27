import os
from utilities.preprocessor import Preprocessor
from models.file import File
from engine.encoder import SemanticIndexer

# Initialize everything
resource_dir = "resources"
preprocessor = Preprocessor(token_threshold=10000)  # or None if no limit
indexer = SemanticIndexer()

# Step 1: Load and preprocess files
documents = []
metadatas = []

for filename in os.listdir(resource_dir):
    if filename == ".DS_Store":
        continue
    path = os.path.join(resource_dir, filename)
    if not os.path.isfile(path):
        continue

    with open(path, "rb") as f:
        content = f.read()

    file = File(content=content, name=filename, path=path)
    text = preprocessor.preprocess(file)

    if not text.strip():
        print(f"[Warning] Skipping {filename}: Empty after preprocessing.")
        continue

    documents.append(text)
    metadatas.append({
        'filepath': path,
        'filename': filename,
    })

# Step 2: Add documents to indexer
indexer.add_documents(documents, metadatas)

# Step 3: Test a search query
query = "Notes about art"

results = indexer.search(query, k=5)

# Step 4: Pretty print results
print("🔎 Top Search Results:")
for meta, score in results:
    formatted = indexer.format_result(meta, score)
    print(formatted)
