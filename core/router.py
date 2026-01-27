
CODING_KEYWORDS = ["code", "python", "java", "bug", "error", "function", "script"]
KNOWLEDGE_KEYWORDS = ["what is", "who is", "explain", "define", "meaning of", "how does", "describe"]
ACTION_KEYWORDS = ["open", "send", "call", "run", "show me", "turn on", "turn off"]
HACKING_KEYWORDS = ["hack", "hacking", "cybersecurity", "penetration testing"]

INTENTS = {
    "coding": CODING_KEYWORDS,
    "knowledge": KNOWLEDGE_KEYWORDS,
    "action": ACTION_KEYWORDS,
    "hacking": HACKING_KEYWORDS
}


def classify_intent(text: str) -> str:
    """
    Classifies the intent of the given text.
    Returns: coding, knowledge, action, hacking, or conversation (default)
    """
    text = text.lower().strip()

    for intent, keywords in INTENTS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "conversation"
