# tools/productivity/reminder.py

import logging
from datetime import datetime

from memory.manager import MemoryManager

logger = logging.getLogger("Tina")

memory = MemoryManager()


# =====================================================
# CREATE REMINDER
# =====================================================

def create_reminder(
    text: str,
    time: str = None,
    priority: int = 7
):

    try:

        # Build structured reminder content
        content = text

        if time:
            content = f"[{time}] {text}"

        memory.remember(
            memory=content,
            category="reminder",
            importance=priority
        )

        logger.info("Reminder saved.")

        return {
            "success": True,
            "message": "Reminder saved successfully.",
            "data": {
                "text": text,
                "time": time,
                "priority": priority,
                "created_at": datetime.now().isoformat()
            }
        }

    except Exception as e:

        logger.error(f"Reminder error: {e}", exc_info=True)

        return {
            "success": False,
            "message": str(e),
            "data": None
        }


# =====================================================
# GET REMINDERS
# =====================================================

def get_reminders(limit: int = 10):

    try:

        reminders = memory.recall(limit=limit)

        formatted = []

        for r in reminders:

            if r["category"] == "reminder":

                formatted.append(r["memory"])

        return {
            "success": True,
            "message": "Reminders retrieved.",
            "data": formatted
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e),
            "data": None
        }


# =====================================================
# FUTURE EXTENSION HOOK (IMPORTANT)
# =====================================================

def parse_time_natural(text: str):
    """
    Placeholder for future upgrade:
    - 'tomorrow 5pm'
    - 'in 2 hours'
    - 'next monday'
    """

    return None