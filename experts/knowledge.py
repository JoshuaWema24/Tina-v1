# experts/knowledge.py

def handle(text: str) -> str:
    """
    Handles factual and informational queries.
    """
    # Local import to avoid circular import
    from core.llm import call_llm

    prompt = f"Answer this clearly and accurately:\n{text}"
    return call_llm(prompt)
