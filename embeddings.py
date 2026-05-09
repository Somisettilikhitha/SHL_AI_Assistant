import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

# -----------------------------------
# MODEL
# -----------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded")

# -----------------------------------
# LOAD CATALOG
# -----------------------------------

with open(
    "catalog.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

# -----------------------------------
# BUILD TEXTS
# -----------------------------------

texts = []

for item in data:

    text = (

        item["name"] + " " +

        item["description"] + " " +

        item["test_type"]

    )

    texts.append(text)

# -----------------------------------
# CREATE EMBEDDINGS
# -----------------------------------

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

print(
    "Embeddings created"
)

# -----------------------------------
# CREATE FAISS INDEX
# -----------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    np.array(embeddings)
)

# -----------------------------------
# SAVE INDEX
# -----------------------------------

faiss.write_index(
    index,
    "shl_index.faiss"
)

print(
    "FAISS index saved"
)