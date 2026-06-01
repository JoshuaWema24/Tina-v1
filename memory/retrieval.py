from memory.long_term import get_memories, search_memories
from memory.embeddings import find_similar_memories


# =====================================================
# 🧠 CONFIG
# =====================================================
SEMANTIC_FALLBACK_LIMIT = 5
KEYWORD_LIMIT = 10


# =====================================================
# 🧠 SAFE MEMORY ACCESS
# =====================================================
def _get_memory_text(memory):
    """
    Handles both old and new DB schemas safely.
    """
    return memory.get("memory") or memory.get("content") or ""


# =====================================================
# 🧠 CLEAN KEYWORDS
# =====================================================
def extract_keywords(text):
    """
    Improved lightweight keyword extraction.
    """

    stop_words = {
        "the", "is", "a", "an", "and", "or", "to", "for",
        "of", "in", "on", "at", "i", "you", "me", "my",
        "it", "am", "was", "were", "are", "do", "did"
    }

    text = text.lower()

    words = [
        w.strip(".,!?()[]{}")
        for w in text.split()
    ]

    return [
        w for w in words
        if w and w not in stop_words
    ]


# =====================================================
# 🧠 RECENT MEMORY CONTEXT
# =====================================================
def get_recent_context(limit=5):
    """
    Fetches latest stored memories.
    """

    memories = get_memories(limit)

    if not memories:
        return ""

    context = ["[RECENT MEMORY]"]

    for memory in memories:
        text = _get_memory_text(memory)
        if text:
            context.append(f"- {text}")

    return "\n".join(context)


# =====================================================
# 🧠 KEYWORD-BASED RETRIEVAL
# =====================================================
def get_keyword_context(user_input):
    """
    Retrieves memories using keyword search.
    """

    keywords = extract_keywords(user_input)

    matched = []
    seen = set()

    for keyword in keywords:
        results = search_memories(keyword)

        for r in results:
            text = _get_memory_text(r)

            if not text:
                continue

            if text not in seen:
                seen.add(text)
                matched.append(text)

    if not matched:
        return ""

    context = ["[RELEVANT MEMORY - KEYWORD MATCH]"]

    for m in matched[:KEYWORD_LIMIT]:
        context.append(f"- {m}")

    return "\n".join(context)


# =====================================================
# 🧠 SEMANTIC RETRIEVAL (EMBEDDINGS)
# =====================================================
def get_semantic_context(user_input):
    """
    Uses embeddings for deeper meaning search.
    """

    try:
        # get all memories as raw text
        all_memories = get_memories(limit=50)

        memory_texts = [
            _get_memory_text(m)
            for m in all_memories
        ]

        memory_texts = [m for m in memory_texts if m]

        if not memory_texts:
            return ""

        results = find_similar_memories(
            query=user_input,
            memories=memory_texts,
            top_k=SEMANTIC_FALLBACK_LIMIT
        )

        if not results:
            return ""

        context = ["[SEMANTIC MEMORY]"]

        for memory, score in results:
            context.append(f"- {memory} (score: {score:.2f})")

        return "\n".join(context)

    except Exception:
        # graceful fallback if embeddings fail
        return ""


# =====================================================
# 🧠 BUILD FINAL CONTEXT (MAIN FUNCTION)
# =====================================================
def build_memory_context(user_input):
    """
    Master retrieval function for Tina.
    Combines:
    - recent memory
    - keyword memory
    - semantic memory
    """

    sections = []

    recent = get_recent_context()
    if recent:
        sections.append(recent)

    keyword = get_keyword_context(user_input)
    if keyword:
        sections.append(keyword)

    semantic = get_semantic_context(user_input)
    if semantic:
        sections.append(semantic)

    return "\n\n".join(sections).strip()