import asyncio
import logging
from datetime import datetime

from memory.reminders import get_due_reminders, complete_reminder

logger = logging.getLogger("Tina")


# =====================================================
# REMINDER HANDLER (HOOK INTO TINA RESPONSE SYSTEM)
# =====================================================

def trigger_reminder(reminder):

    text = reminder["reminder_text"]

    logger.info(f"🔔 Reminder triggered: {text}")

    # HERE is where Jarvis-style behavior happens:
    # You can later push this into:
    # - CLI notification
    # - speech synthesis
    # - UI popup
    # - LLM context injection

    print(f"\n🔔 REMINDER: {text}\n")


    # mark as done
    complete_reminder(reminder["id"])


# =====================================================
# MAIN LOOP (JARVIS BACKGROUND BRAIN)
# =====================================================

async def reminder_loop(interval: int = 10):
    """
    Continuously checks for due reminders.
    """

    logger.info("⏰ Reminder scheduler started.")

    while True:

        try:

            reminders = get_due_reminders()

            if reminders:

                for reminder in reminders:

                    trigger_reminder(reminder)

            await asyncio.sleep(interval)

        except Exception as e:

            logger.error(
                f"Reminder scheduler error: {e}",
                exc_info=True
            )

            await asyncio.sleep(interval)