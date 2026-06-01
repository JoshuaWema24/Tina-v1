# tools/productivity/notes.py

import logging
from memory.manager import MemoryManager

logger = logging.getLogger("Tina")

memory = MemoryManager()


# =====================================================
# CREATE NOTE
# =====================================================

def create_note(text: str, title: str = None, importance: int = 5):

    try:

        content = text

        if title:
            content = f"{title}: {text}"

        memory.remember(
            memory=content,
            category="notes",
            importance=importance
        )

        logger.info("Note saved successfully.")

        return {
            "success": True,
            "message": "Note saved successfully.",
            "data": {
                "title": title,
                "content": text
            }
        }

    except Exception as e:

        logger.error(f"Notes error: {e}", exc_info=True)

        return {
            "success": False,
            "message": str(e),
            "data": None
        }


# =====================================================
# GET NOTES
# =====================================================

def get_notes(limit: int = 10):

    try:

        notes = memory.recall(limit=limit)

        formatted = []

        for n in notes:

            if n["category"] == "notes":

                formatted.append(n["memory"])

        return {
            "success": True,
            "message": "Notes retrieved.",
            "data": formatted
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e),
            "data": None
        }