import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Load chunks from the pickle file
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {len(chunks)} chunks")

# Load the embedding model 
model = SentenceTransformer("all-mpnet-base-v2") 

# Prepare a list of texts to embed (just the content field)
texts = [chunk["content"] for chunk in chunks]

# Generate embeddings for all chunks
embeddings = model.encode(texts, show_progress_bar=True)

print(f"Generated {len(embeddings)} embeddings")

# Save both chunks and embeddings together for easy lookup later
data = {
    "chunks": chunks,
    "embeddings": embeddings,
}

# Check for NaNs
invalids = [i for i, vec in enumerate(embeddings) if not np.isfinite(vec).all()]
print(f"Invalid vectors: {len(invalids)}")

with open("embeddings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Saved embeddings and chunks to embeddings.pkl")
