from database.db import get_connection
from memory.embeddings import embed_text
import hashlib
import json
from datetime import datetime


# =====================================
# UTILITY: CREATE MEMORY HASH (DEDUP)
# =====================================
def create_hash(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


# =====================================
# SAVE MEMORY (SMART + EMBEDDINGS)
# =====================================
def save_memory(memory, category="general", importance=5, metadata=None):
    """
    Saves memory with embedding + deduplication.
    """

    conn = get_connection()
    cursor = conn.cursor()

    memory_hash = create_hash(memory)

    # Check duplicates
    cursor.execute("""
        SELECT id FROM memories WHERE hash = ?
    """, (memory_hash,))

    if cursor.fetchone():
        conn.close()
        return False  # duplicate ignored

    embedding = embed_text(memory)

    cursor.execute("""
        INSERT INTO memories (
            memory,
            category,
            importance,
            hash,
            embedding,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        memory,
        category,
        importance,
        memory_hash,
        json.dumps(embedding),
        datetime.utcnow()
    ))

    conn.commit()
    conn.close()

    return True


# =====================================
# GET RECENT MEMORIES
# =====================================
def get_memories(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM memories
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# =====================================
# SEARCH BY TEXT (HYBRID SEARCH)
# =====================================
def search_memories(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM memories
        WHERE memory LIKE ?
        ORDER BY importance DESC, created_at DESC
    """, (f"%{keyword}%",))

    rows = cursor.fetchall()
    conn.close()

    return rows


# =====================================
# SEMANTIC SEARCH (JARVIS CORE)
# =====================================
def semantic_search(query_embedding, limit=5):
    """
    Finds memories based on meaning, not keywords.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, memory, embedding, importance
        FROM memories
    """)

    rows = cursor.fetchall()

    scored = []

    for row in rows:
        memory_embedding = json.loads(row["embedding"])

        score = cosine_similarity(query_embedding, memory_embedding)

        scored.append((score, row))

    scored.sort(reverse=True, key=lambda x: x[0])

    conn.close()

    return [row for score, row in scored[:limit]]


# =====================================
# DELETE MEMORY
# =====================================
def delete_memory(memory_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM memories WHERE id = ?
    """, (memory_id,))

    conn.commit()
    conn.close()


# =====================================
# GET BY CATEGORY
# =====================================
def get_memories_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM memories
        WHERE category = ?
        ORDER BY importance DESC, created_at DESC
    """, (category,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# =====================================
# COSINE SIMILARITY (LOCAL VECTOR SEARCH)
# =====================================
def cosine_similarity(a, b):
    import math

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)