# core/router.py

def classify_intent(text: str) -> str:
    text = text.lower().strip()

    # ---- Coding intent ----
    if any(keyword in text for keyword in [
        "code", "python", "java", "bug", "error", "function", "script"
    ]):
        return "coding"

    # ---- Knowledge intent ----
    if any(keyword in text for keyword in [
        "what is", "who is", "explain", "define",
        "meaning of", "how does", "describe"
    ]):
        return "knowledge"

    # ---- Action intent (physical / system actions) ----
    if any(keyword in text for keyword in [
        "open", "send", "call", "run", "show me", "turn on", "turn off"
    ]):
        return "action"

    # ---- Cybersecurity / ethical discussion only ----
    if any(keyword in text for keyword in [
        "hack", "hacking", "cybersecurity", "penetration testing"
    ]):
        return "hacking"

    # ---- Default ----
    return "conversation"
