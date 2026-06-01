from typing import List, Dict
from datetime import datetime

# ==========================
# CONFIG
# ==========================
MAX_TURNS = 12

# ==========================
# IN-MEMORY STORAGE
# ==========================
_conversation: List[Dict[str, str]] = []

_session_id = "default"


# ==========================
# SESSION CONTROL (JARVIS READY)
# ==========================
def set_session(session_id: str):
    global _session_id
    _session_id = session_id


def get_session():
    return _session_id


# ==========================
# ADD CONVERSATION TURN
# ==========================
def add(user_message: str, assistant_message: str):
    """
    Store a conversation turn in short-term memory.
    """

    global _conversation

    _conversation.append({
        "session_id": _session_id,
        "user": user_message.strip(),
        "assistant": assistant_message.strip(),
        "timestamp": datetime.utcnow().isoformat()
    })

    # Keep rolling window
    if len(_conversation) > MAX_TURNS:
        _conversation = _conversation[-MAX_TURNS:]


# ==========================
# GET RAW MEMORY
# ==========================
def get() -> List[Dict[str, str]]:
    return _conversation


# ==========================
# FORMAT FOR LLM (JARVIS CONTEXT STYLE)
# ==========================
def format_for_prompt() -> str:
    """
    Converts memory into clean LLM context.
    """

    if not _conversation:
        return ""

    lines = []

    for turn in _conversation:
        lines.append(f"User: {turn['user']}")
        lines.append(f"Tina: {turn['assistant']}")

    return "\n".join(lines)


# ==========================
# GET RECENT CONTEXT
# ==========================
def get_recent_context(limit=6) -> str:
    """
    Returns most recent conversation context.
    """

    if not _conversation:
        return ""

    recent = _conversation[-limit:]

    lines = []

    for turn in recent:
        lines.append(f"User: {turn['user']}")
        lines.append(f"Tina: {turn['assistant']}")

    return "\n".join(lines)


# ==========================
# LAST MESSAGES (FOR INTENT ENGINE)
# ==========================
def last_user_message() -> str:
    return _conversation[-1]["user"] if _conversation else ""


def last_tina_message() -> str:
    return _conversation[-1]["assistant"] if _conversation else ""


# ==========================
# CLEAR MEMORY
# ==========================
def clear():
    global _conversation
    _conversation = []


# ==========================
# MEMORY SIZE
# ==========================
def size() -> int:
    return len(_conversation)


# ==========================
# EXPORT FOR LONG-TERM MEMORY SYSTEM
# ==========================
def export_for_memory():
    """
    Converts short-term memory into
    long-term ingestion format.
    """

    return [
        {
            "session_id": _session_id,
            "user": turn["user"],
            "assistant": turn["assistant"],
            "timestamp": turn["timestamp"]
        }
        for turn in _conversation
    ]