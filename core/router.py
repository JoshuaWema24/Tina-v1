def classify_intent(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["open", "send", "call", "run"]):
        return "action"

    if any(word in text for word in ["code", "python", "bug", "error"]):
        return "coding"

    if any(word in text for word in [
        "what is", "who is", "explain", "define", "meaning", "how does"
    ]):
        return "knowledge"

    return "conversation"
