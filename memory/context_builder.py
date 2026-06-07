from memory.short_term import format_for_prompt
from memory.retrieval import build_memory_context
from memory.long_term import get_memories
from memory.embeddings import find_similar_memories
from memory.state import state

# =====================================================
# 🧠 BUILD FULL CONTEXT (FUSION LAYER)
# =====================================================

def build_context(user_input: str):

    # -----------------------------
    # 1. SHORT TERM MEMORY
    # -----------------------------
    short_context = format_for_prompt()

    # -----------------------------
    # 2. LONG TERM MEMORY
    # -----------------------------
    long_context = build_memory_context(user_input)

    # -----------------------------
    # 3. SEMANTIC MEMORY (FUTURE-READY)
    # -----------------------------
    semantic_context = ""

    try:
        memories = get_memories(limit=50)

        memory_texts = [
            m["memory"] for m in memories
        ]

        similar = find_similar_memories(
            user_input,
            memory_texts,
            top_k=3
        )

        if similar:
            semantic_context = "Relevant Semantic Memory:\n"

            for mem, score in similar:
                semantic_context += f"- {mem} (score: {score:.2f})\n"

    except Exception:
        semantic_context = ""

    # -----------------------------
    # FINAL FUSED CONTEXT
    # -----------------------------
    final_context = "\n\n".join(
        section for section in [
            short_context,
            long_context,
            semantic_context
        ] if section
    )

    return final_context

def build_state_context():

    context = []

    if state.active_project:
        context.append(
            f"Active Project: {state.active_project}"
        )

    if state.current_topic:
        context.append(
            f"Current Topic: {state.current_topic}"
        )

    if state.current_goal:
        context.append(
            f"Current Goal: {state.current_goal}"
        )

    return "\n".join(context)