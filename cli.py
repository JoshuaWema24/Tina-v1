import logging
import asyncio

from core.orchestrator import process
from database.db import init_db


async def main():

    # ==========================
    # INITIALIZE DATABASE
    # ==========================
    init_db()

    # ==========================
    # LOGGING SETUP
    # ==========================
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Tina")

    # ==========================
    # STARTUP MESSAGE
    # ==========================
    print("\n🤖 Tina AI CLI (Ollama Powered)")
    print("Type 'exit' or 'quit' to stop.\n")

    # ==========================
    # MAIN LOOP
    # ==========================
    while True:

        try:
            # Get user input asynchronously
            user_input = await asyncio.to_thread(input, "You: ")
            user_input = user_input.strip()

            # Ignore empty input
            if not user_input:
                continue

            # Exit commands
            if user_input.lower() in ["exit", "quit"]:
                print("Tina: Goodbye 👋")
                break

            # ==========================
            # PROCESS THROUGH ORCHESTRATOR
            # ==========================
            result = await process(user_input)

            # ==========================
            # SAFE OUTPUT HANDLING
            # ==========================
            if isinstance(result, dict):

                if result.get("type") == "chat":
                    print(f"Tina: {result.get('reply', '')}\n")

                elif result.get("type") == "action":
                    print(f"Tina (action): {result.get('reply', '')}\n")

                else:
                    print(f"Tina: {result}\n")

            else:
                print(f"Tina: {result}\n")

        except KeyboardInterrupt:
            print("\nTina: Interrupted. Bye 👋")
            break

        except Exception as e:
            logger.error(f"Error: {e}")
            print("Tina: Something went wrong. Try again.\n")


# ==========================
# ENTRY POINT
# ==========================
if __name__ == "__main__":
    asyncio.run(main())