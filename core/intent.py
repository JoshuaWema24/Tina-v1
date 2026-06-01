import re

# =====================================================
# 🧠 KEYWORDS
# (kept for fallback classification)
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

# =====================================================
# 🧠 ACTION INTENT PARSER (IMPORTANT FIX)
# =====================================================

def parse_action(text: str):
    """
    Extracts actionable command + target.
    Example:
        "open chrome" → ("open_app", "chrome")
    """

    text = text.lower().strip()

    # OPEN / LAUNCH APP
    match = re.search(r"(open|launch|start)\s+(.+)", text)
    if match:
        target = match.group(2).strip()

        return {
            "intent": "action",
            "tool": "open_app",
            "target": target
        }

    # CLOSE APP
    match = re.search(r"(close|exit|quit)\s+(.+)", text)
    if match:
        target = match.group(2).strip()

        return {
            "intent": "action",
            "tool": "close_app",
            "target": target
        }

    # PLAY MEDIA
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
# 🧠 MAIN CLASSIFIER
# =====================================================

def classify_intent(text: str):
    text = text.lower().strip()

    # =========================
    # 1. ACTION CHECK FIRST
    # =========================
    action = parse_action(text)
    if action:
        return action

    # =========================
    # 2. CODING
    # =========================
    if any(k in text for k in CODING_KEYWORDS):
        return {
            "intent": "coding"
        }

    # =========================
    # 3. KNOWLEDGE
    # =========================
    if any(k in text for k in KNOWLEDGE_KEYWORDS):
        return {
            "intent": "knowledge"
        }

    # =========================
    # 4. SECURITY
    # =========================
    if any(k in text for k in SECURITY_KEYWORDS):
        return {
            "intent": "security"
        }

    # =========================
    # 5. EMOTION
    # =========================
    if any(k in text for k in EMOTION_KEYWORDS):
        return {
            "intent": "emotion"
        }

    # =========================
    # 6. DEFAULT CONVERSATION
    # =========================
    return {
        "intent": "conversation"
    }


# =====================================================
# 🧠 OPTIONAL MULTI-INTENT (FUTURE UPGRADE HOOK)
# =====================================================

def classify_intents(text: str):
    """
    Future: multi-intent support (not used yet).
    """

    intents = []

    if any(k in text.lower() for k in CODING_KEYWORDS):
        intents.append("coding")

    if any(k in text.lower() for k in KNOWLEDGE_KEYWORDS):
        intents.append("knowledge")

    if any(k in text.lower() for k in SECURITY_KEYWORDS):
        intents.append("security")

    if any(k in text.lower() for k in EMOTION_KEYWORDS):
        intents.append("emotion")

    if not intents:
        intents.append("conversation")

    return intents