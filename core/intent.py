import re

# =====================================================
# 🧠 KEYWORDS
# =====================================================

CODING_KEYWORDS = [
    "code", "python", "java", "bug", "error", "function",
    "script", "programming", "developer", "coding", "debug"
]

KNOWLEDGE_KEYWORDS = [
    "what is", "who is", "explain", "define", "meaning of",
    "how does", "describe", "tell me about"
]

SECURITY_KEYWORDS = [
    "hack", "hacking", "cybersecurity", "penetration testing",
    "exploit", "vulnerability", "security"
]

EMOTION_KEYWORDS = [
    "sad", "happy", "bored", "angry", "lonely",
    "tired", "stressed", "frustrated", "excited"
]

ACTION_VERBS = [
    "open", "launch", "start", "close", "exit",
    "quit", "play", "run", "take", "capture", "record"
]

# =====================================================
# 🧠 ACTION INTENT PARSER
# =====================================================

def parse_action(text: str):

    text = text.lower().strip()

    match = re.search(r"(open|launch|start)\s+(.+)", text)
    if match:
        target = match.group(2).strip()
        return {
            "intent": "action",
            "tool": "open_app",
            "target": target
        }

    match = re.search(r"(close|exit|quit)\s+(.+)", text)
    if match:
        target = match.group(2).strip()
        return {
            "intent": "action",
            "tool": "close_app",
            "target": target
        }

    match = re.search(r"(play)\s+(.+)", text)
    if match:
        target = match.group(2).strip()
        return {
            "intent": "action",
            "tool": "play_media",
            "target": target
        }

    return None


# =====================================================
# 🧠 SINGLE INTENT CLASSIFIER
# =====================================================

def classify_intent(text: str):
    text = text.lower().strip()

    action = parse_action(text)
    if action:
        return action

    if any(k in text for k in CODING_KEYWORDS):
        return {"intent": "coding"}

    if any(k in text for k in KNOWLEDGE_KEYWORDS):
        return {"intent": "knowledge"}

    if any(k in text for k in SECURITY_KEYWORDS):
        return {"intent": "security"}

    if any(k in text for k in EMOTION_KEYWORDS):
        return {"intent": "emotion"}

    return {"intent": "conversation"}


# =====================================================
# 🧠 MULTI-INTENT CLASSIFIER (used by router)
# =====================================================

def classify_intents(text: str):

    intents = []
    lower = text.lower()

    # ── ACTION (checked first, highest priority) ──
    if parse_action(lower):
        intents.append("action")

    # ── CODING ──
    if any(k in lower for k in CODING_KEYWORDS):
        intents.append("coding")

    # ── KNOWLEDGE ──
    if any(k in lower for k in KNOWLEDGE_KEYWORDS):
        intents.append("knowledge")

    # ── SECURITY ──
    if any(k in lower for k in SECURITY_KEYWORDS):
        intents.append("security")

    # ── EMOTION ──
    if any(k in lower for k in EMOTION_KEYWORDS):
        intents.append("emotion")

    # ── FALLBACK ──
    if not intents:
        intents.append("conversation")

    return intents