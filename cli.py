import logging
import asyncio

from core.orchestrator import process
from database.db import init_db
from core.reminder_scheduler import reminder_loop


# =====================================================
# MAIN CLI LOOP
# =====================================================

async def cli_loop():

    print("\n🤖 Tina AI CLI (Ollama Powered)")
    print("Type 'exit' or 'quit' to stop.\n")

    logger = logging.getLogger("Tina")

    while True:

        try:

            user_input = await asyncio.to_thread(
                input,
                "You: "
            )

            user_input = user_input.strip()

            if not user_input:

                continue

            if user_input.lower() in [
                "exit",
                "quit"
            ]:

                print("Tina: Goodbye 👋")

                break

            # ==========================
            # PROCESS ORCHESTRATOR
            # ==========================

            result = await process(user_input)

            # ==========================
            # OUTPUT HANDLING
            # ==========================

            if isinstance(result, dict):

                if result.get("type") == "chat":

                    print(
                        f"Tina: {result.get('reply','')}\n"
                    )

                elif result.get("type") == "action":

                    print(
                        f"Tina (action): {result.get('reply','')}\n"
                    )

                else:

                    print(f"Tina: {result}\n")

            else:

                print(f"Tina: {result}\n")

        except KeyboardInterrupt:

            print("\nTina: Interrupted 👋")

            break

        except Exception as e:

            logger.error(f"CLI Error: {e}")

            print("Tina: Something went wrong.\n")


# =====================================================
# SYSTEM BOOTSTRAP
# =====================================================

async def main():

    # --------------------------
    # INIT DATABASE
    # --------------------------
    init_db()

    # --------------------------
    # LOGGING
    # --------------------------
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("Tina")

    logger.info("Starting Tina system...")

    # --------------------------
    # START BACKGROUND SERVICES
    # --------------------------
    asyncio.create_task(reminder_loop())

    # --------------------------
    # START CLI
    # --------------------------
    await cli_loop()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    asyncio.run(main())