from database.db import get_connection


# =====================================
# SAVE MEMORY
# =====================================
def save_memory(
    memory,
    category="general",
    importance=5
):
    """
    Saves a memory into the database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO memories (
        memory,
        category,
        importance
    )
    VALUES (?, ?, ?)
    """, (
        memory,
        category,
        importance
    ))

    conn.commit()
    conn.close()


# =====================================
# GET RECENT MEMORIES
# =====================================
def get_memories(limit=10):
    """
    Returns recent memories.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM memories
    ORDER BY created_at DESC
    LIMIT ?
    """, (limit,))

    memories = cursor.fetchall()

    conn.close()

    return memories


# =====================================
# SEARCH MEMORIES
# =====================================
def search_memories(keyword):
    """
    Searches memories using a keyword.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM memories
    WHERE memory LIKE ?
    ORDER BY created_at DESC
    """, (f"%{keyword}%",))

    memories = cursor.fetchall()

    conn.close()

    return memories


# =====================================
# DELETE MEMORY
# =====================================
def delete_memory(memory_id):
    """
    Deletes a memory by ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM memories
    WHERE id = ?
    """, (memory_id,))

    conn.commit()
    conn.close()


# =====================================
# GET MEMORIES BY CATEGORY
# =====================================
def get_memories_by_category(category):
    """
    Returns memories from a specific category.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM memories
    WHERE category = ?
    ORDER BY created_at DESC
    """, (category,))

    memories = cursor.fetchall()

    conn.close()

    return memories