from core.llm import call_llm

def handle(text: str) -> str:
    return call_llm(text)
