# experts/conversation.py

def handle(text: str) -> str:
    """
    Handles conversation-related queries.
    """
    # Local import to avoid circular import
    from core.llm import call_llm

    prompt = f"Have a friendly conversation with:\n{text}"
    return call_llm(prompt)
