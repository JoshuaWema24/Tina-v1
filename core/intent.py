# core/intent.py

# =====================================================
# 🧠 CODING
# =====================================================

CODING_KEYWORDS = [
    "code",
    "python",
    "java",
    "bug",
    "error",
    "function",
    "script",
    "programming",
    "developer",
    "coding",
    "debug"
]

# =====================================================
# 🧠 KNOWLEDGE
# =====================================================

KNOWLEDGE_KEYWORDS = [
    "what is",
    "who is",
    "explain",
    "define",
    "meaning of",
    "how does",
    "describe",
    "tell me about"
]

# =====================================================
# 🧠 ACTIONS
# =====================================================

ACTION_KEYWORDS = [
    "open",
    "send",
    "call",
    "run",
    "launch",
    "start",
    "show me",
    "turn on",
    "turn off",
    "close",
    "play"
]

# =====================================================
# 🧠 SECURITY
# =====================================================

SECURITY_KEYWORDS = [
    "hack",
    "hacking",
    "cybersecurity",
    "penetration testing",
    "exploit",
    "vulnerability",
    "security"
]

# =====================================================
# 🧠 EMOTIONS
# =====================================================

EMOTION_KEYWORDS = [
    "sad",
    "happy",
    "bored",
    "angry",
    "lonely",
    "tired",
    "stressed",
    "frustrated",
    "excited"
]

# =====================================================
# 🧠 INTENT MAP
# =====================================================

INTENT_MAP = {
    "coding": CODING_KEYWORDS,
    "knowledge": KNOWLEDGE_KEYWORDS,
    "action": ACTION_KEYWORDS,
    "security": SECURITY_KEYWORDS,
    "emotion": EMOTION_KEYWORDS
}


# =====================================================
# 🧠 MULTI-INTENT CLASSIFIER
# =====================================================

def classify_intents(text: str):

    text = text.lower().strip()

    detected = []

    for intent, keywords in INTENT_MAP.items():

        if any(keyword in text for keyword in keywords):

            detected.append(intent)

    # =================================================
    # DEFAULT FALLBACK
    # =================================================

    if not detected:
        detected.append("conversation")

    return detected


# =====================================================
# 🧠 SINGLE INTENT (BACKWARD COMPATIBILITY)
# =====================================================

def classify_intent(text: str) -> str:

    intents = classify_intents(text)

    return intents[0]