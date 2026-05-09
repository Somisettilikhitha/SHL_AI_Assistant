import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

print("Loading embedding model...")

# -----------------------------------
# Load Embedding Model
# -----------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded successfully")

# -----------------------------------
# Load FAISS Index
# -----------------------------------

index = faiss.read_index(
    "shl_index.faiss"
)

print("FAISS index loaded")

# -----------------------------------
# Load Catalog
# -----------------------------------

with open(
    "catalog.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

print("Catalog loaded")

# -----------------------------------
# BM25 Corpus
# -----------------------------------

corpus = []

for item in data:

    text = (

        item["name"] + " " +

        item["description"] + " " +

        item["test_type"]

    )

    corpus.append(
        text.split()
    )

# -----------------------------------
# Initialize BM25
# -----------------------------------

bm25 = BM25Okapi(corpus)

print("BM25 initialized")

# -----------------------------------
# Hybrid Retrieval
# -----------------------------------

def retrieve_assessments(
    query,
    top_k=5
):

    print("Searching for:", query)

    # -----------------------------------
    # Semantic Search
    # -----------------------------------

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(

        np.array(query_embedding),

        top_k * 3
    )

    semantic_results = []

    for idx in indices[0]:

        semantic_results.append(
            data[idx]
        )

    # -----------------------------------
    # BM25 Search
    # -----------------------------------

    tokenized_query = (
        query.lower().split()
    )

    bm25_scores = bm25.get_scores(
        tokenized_query
    )

    bm25_indices = np.argsort(
        bm25_scores
    )[::-1][:top_k * 3]

    keyword_results = []

    for idx in bm25_indices:

        keyword_results.append(
            data[idx]
        )

    # -----------------------------------
    # Combine Results
    # -----------------------------------

    combined_results = (
        semantic_results +
        keyword_results
    )

    # -----------------------------------
    # Smart Scoring
    # -----------------------------------

    scored_results = []

    query_lower = query.lower()

    for item in combined_results:

        score = 1

        name_lower = (
            item["name"].lower()
        )

        desc_lower = (
            item["description"].lower()
        )

        test_type_lower = (
            item["test_type"].lower()
        )

        # -----------------------------------
        # AWS / CLOUD BOOST
        # -----------------------------------

        if (

            "aws" in query_lower
            or
            "cloud" in query_lower

        ):

            if (

                "aws" in name_lower
                or
                "cloud" in name_lower

            ):

                score += 8

            if (

                "remoteworkq" in name_lower

            ):

                score -= 5

        # -----------------------------------
        # PYTHON BOOST
        # -----------------------------------

        if "python" in query_lower:

            if "python" in name_lower:

                score += 8

        # -----------------------------------
        # JAVA BOOST
        # -----------------------------------

        if "java" in query_lower:

            if "java" in name_lower:

                score += 8

        # -----------------------------------
        # JAVASCRIPT BOOST
        # -----------------------------------

        if "javascript" in query_lower:

            if (

                "javascript" in name_lower
                or
                "react" in name_lower
                or
                "frontend" in name_lower

            ):

                score += 8

        # -----------------------------------
        # COGNITIVE BOOST
        # -----------------------------------

        if (

            "cognitive" in query_lower
            or
            "aptitude" in query_lower
            or
            "reasoning" in query_lower

        ):

            if (

                "gsa" in name_lower
                or
                "general ability" in name_lower
                or
                "verify" in name_lower
                or
                "reasoning" in desc_lower

            ):

                score += 8

        # -----------------------------------
        # PERSONALITY BOOST
        # -----------------------------------

        if (

            "leadership" in query_lower
            or
            "personality" in query_lower

        ):

            if (

                "opq" in name_lower
                or
                "leadership" in name_lower
                or
                "personality" in desc_lower

            ):

                score += 8

        # -----------------------------------
        # FINANCE BOOST
        # -----------------------------------

        if (

            "finance" in query_lower
            or
            "accounting" in query_lower
            or
            "banking" in query_lower

        ):

            if (

                "finance" in test_type_lower
                or
                "accounting" in desc_lower
                or
                "banking" in desc_lower

            ):

                score += 8

        # -----------------------------------
        # SALES BOOST
        # -----------------------------------

        if (

            "sales" in query_lower
            or
            "retail" in query_lower

        ):

            if (

                "sales" in desc_lower
                or
                "retail" in desc_lower

            ):

                score += 8

        scored_results.append(
            (score, item)
        )

    # -----------------------------------
    # Sort by Score
    # -----------------------------------

    scored_results.sort(

        key=lambda x: x[0],

        reverse=True
    )

    # -----------------------------------
    # Remove Duplicates
    # -----------------------------------

    final_results = []

    seen = set()

    for score, item in scored_results:

        if item["url"] not in seen:

            seen.add(
                item["url"]
            )

            final_results.append(
                item
            )

    # -----------------------------------
    # Return Top Results
    # -----------------------------------

    return final_results[:top_k]

# -----------------------------------
# Direct Testing
# -----------------------------------

if __name__ == "__main__":

    query = "AWS cloud engineer"

    results = retrieve_assessments(
        query
    )

    print("\nTop Results:\n")

    for item in results:

        print(item)