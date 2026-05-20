# memory/short_term.py

from typing import List, Dict

# ==========================
# CONFIG
# ==========================
MAX_TURNS = 10


# ==========================
# MEMORY STORAGE
# ==========================
"""
Each memory item looks like:

{
    "user": "...",
    "assistant": "..."
}
"""

_conversation: List[Dict[str, str]] = []


# ==========================
# ADD CONVERSATION TURN
# ==========================
def add(
    user_message: str,
    assistant_message: str
) -> None:
    """
    Adds a conversation exchange
    into short-term memory.
    """

    global _conversation

    _conversation.append({
        "user": user_message.strip(),
        "assistant": assistant_message.strip()
    })

    # Keep only recent turns
    if len(_conversation) > MAX_TURNS:
        _conversation = _conversation[-MAX_TURNS:]


# ==========================
# GET RAW MEMORY
# ==========================
def get() -> List[Dict[str, str]]:
    """
    Returns raw short-term memory.
    """

    return _conversation


# ==========================
# FORMAT FOR PROMPT
# ==========================
def format_for_prompt() -> str:
    """
    Converts conversation history
    into prompt-friendly format.
    """

    if not _conversation:
        return ""

    lines = []

    for turn in _conversation:

        lines.append(
            f"User: {turn['user']}"
        )

        lines.append(
            f"Tina: {turn['assistant']}"
        )

    return "\n".join(lines)


# ==========================
# GET RECENT CONTEXT
# ==========================
def get_recent_context(limit=5) -> str:
    """
    Returns recent conversation context.
    """

    if not _conversation:
        return ""

    recent_turns = _conversation[-limit:]

    lines = []

    for turn in recent_turns:

        lines.append(
            f"User: {turn['user']}"
        )

        lines.append(
            f"Tina: {turn['assistant']}"
        )

    return "\n".join(lines)


# ==========================
# CLEAR MEMORY
# ==========================
def clear() -> None:
    """
    Clears short-term memory.
    """

    global _conversation

    _conversation = []


# ==========================
# GET LAST USER MESSAGE
# ==========================
def last_user_message() -> str:

    if not _conversation:
        return ""

    return _conversation[-1]["user"]


# ==========================
# GET LAST TINA MESSAGE
# ==========================
def last_tina_message() -> str:

    if not _conversation:
        return ""

    return _conversation[-1]["assistant"]


# ==========================
# MEMORY SIZE
# ==========================
def size() -> int:
    """
    Returns current memory size.
    """

    return len(_conversation)