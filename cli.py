import logging
import asyncio

from core.orchestrator import process


async def main():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Tina")

    print("\n🤖 Tina AI CLI (Ollama Powered)")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        try:
            user_input = await asyncio.to_thread(input, "You: ")
            user_input = user_input.strip()

            if not user_input:
                continue

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


if __name__ == "__main__":
    asyncio.run(main())