from sentence_transformers import SentenceTransformer
import numpy as np


# =====================================
# LOAD EMBEDDING MODEL
# =====================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================
# CREATE EMBEDDING
# =====================================
def create_embedding(text):
    """
    Converts text into a vector embedding.
    """

    embedding = model.encode(text)

    return embedding


# =====================================
# COSINE SIMILARITY
# =====================================
def cosine_similarity(vec1, vec2):
    """
    Measures similarity between two vectors.
    """

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1)
        * np.linalg.norm(vec2)
    )

    return similarity


# =====================================
# FIND MOST SIMILAR MEMORIES
# =====================================
def find_similar_memories(
    query,
    memories,
    top_k=3
):
    """
    Finds memories most similar to the query.
    
    memories should be a list of strings.
    """

    query_embedding = create_embedding(query)

    scored_memories = []

    for memory in memories:

        memory_embedding = create_embedding(memory)

        similarity = cosine_similarity(
            query_embedding,
            memory_embedding
        )

        scored_memories.append(
            (memory, similarity)
        )

    # Sort by similarity descending
    scored_memories.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored_memories[:top_k]


# =====================================
# FORMAT RESULTS
# =====================================
def format_similar_memories(results):
    """
    Formats similarity results into readable text.
    """

    if not results:
        return ""

    output = "Relevant Semantic Memories:\n"

    for memory, score in results:

        output += (
            f"- {memory} "
            f"(similarity: {score:.2f})\n"
        )

    return output