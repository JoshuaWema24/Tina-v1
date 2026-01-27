# cli.py

import asyncio
from core.router import classify_intent
from experts import conversation, coding, knowledge, hacking, action


async def run_cli():
    print("🤖 Tina is running")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You > ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "shutdown", "sleep"]:
            print("Tina > Goodbye!")
            break

        intent = classify_intent(user_input)

        try:
            if intent == "coding":
                response = coding.handle(user_input)

            elif intent == "knowledge":
                response = knowledge.handle(user_input)

            elif intent == "hacking":
                # If hacking is async, use await; otherwise remove await
                if asyncio.iscoroutinefunction(hacking.handle):
                    response = await hacking.handle(user_input)
                else:
                    response = hacking.handle(user_input)

            elif intent == "action":
                # If action is async
                if asyncio.iscoroutinefunction(action.handle):
                    response = await action.handle(user_input)
                else:
                    response = action.handle(user_input)

            else:  # conversation
                response = await conversation.handle(user_input)

        except Exception as e:
            response = f"⚠️ Error: {e}"

        print(f"Tina ({intent}) > {response}\n")


if __name__ == "__main__":
    asyncio.run(run_cli())
