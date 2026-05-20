from memory.long_term import (
    get_memories,
    search_memories
)


# =====================================
# GET RECENT CONTEXT
# =====================================
def get_recent_context(limit=5):
    """
    Retrieves recent memories and formats them
    into readable context for Tina.
    """

    memories = get_memories(limit)

    if not memories:
        return ""

    context = "Recent Memories:\n"

    for memory in memories:
        context += f"- {memory['memory']}\n"

    return context


# =====================================
# GET RELEVANT CONTEXT
# =====================================
def get_relevant_context(user_input):
    """
    Retrieves memories related to the user's input.
    """

    keywords = extract_keywords(user_input)

    matched_memories = []

    for keyword in keywords:

        results = search_memories(keyword)

        for result in results:

            memory_text = result["memory"]

            if memory_text not in matched_memories:
                matched_memories.append(memory_text)

    if not matched_memories:
        return ""

    context = "Relevant Memories:\n"

    for memory in matched_memories:
        context += f"- {memory}\n"

    return context


# =====================================
# SIMPLE KEYWORD EXTRACTION
# =====================================
def extract_keywords(text):
    """
    Very basic keyword extraction.
    Later this can be replaced with:
    - NLP
    - embeddings
    - semantic search
    """

    stop_words = {
        "the",
        "is",
        "a",
        "an",
        "and",
        "or",
        "to",
        "for",
        "of",
        "in",
        "on",
        "at",
        "i",
        "you",
        "me",
        "my",
        "it"
    }

    words = text.lower().split()

    keywords = [
        word.strip(".,!?")
        for word in words
        if word not in stop_words
    ]

    return keywords


# =====================================
# BUILD FULL MEMORY CONTEXT
# =====================================
def build_memory_context(user_input):
    """
    Combines:
    - recent memories
    - relevant memories
    into one context block.
    """

    recent_context = get_recent_context()
    relevant_context = get_relevant_context(user_input)

    full_context = ""

    if recent_context:
        full_context += recent_context + "\n"

    if relevant_context:
        full_context += relevant_context

    return full_context.strip()