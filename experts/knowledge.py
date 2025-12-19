from core.llm import call_llm

def handle(text: str) -> str:
    """
    Handles factual and informational queries
    """
    prompt = f"Answer this clearly and accurately:\n{text}"
    return call_llm(prompt)
