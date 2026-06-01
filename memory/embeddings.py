from sentence_transformers import SentenceTransformer
import numpy as np

# =====================================
# LOAD MODEL (ONCE)
# =====================================
model = SentenceTransformer("all-MiniLM-L6-v2")


# =====================================
# MAIN JARVIS EMBEDDING FUNCTION
# =====================================
def embed_text(text: str):
    """
    Standard embedding function used by all memory systems.
    """

    vector = model.encode(text)

    return vector.tolist()


# =====================================
# ALIAS (BACKWARD COMPATIBILITY)
# =====================================
def create_embedding(text: str):
    """
    Alias for embed_text (keeps old code working).
    """
    return embed_text(text)


# =====================================
# COSINE SIMILARITY
# =====================================
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


# =====================================
# FIND SIMILAR MEMORIES
# =====================================
def find_similar_memories(query, memories, top_k=3):
    """
    Semantic search over memory list.
    """

    query_embedding = embed_text(query)

    scored = []

    for memory in memories:
        memory_embedding = embed_text(memory)

        score = cosine_similarity(query_embedding, memory_embedding)

        scored.append((memory, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:top_k]


# =====================================
# FORMAT RESULTS
# =====================================
def format_similar_memories(results):
    if not results:
        return ""

    text = "Relevant Semantic Memories:\n"

    for memory, score in results:
        text += f"- {memory} (score: {score:.2f})\n"

    return text