# cli.py

from core.router import classify_intent
from experts import conversation, coding, knowledge

def run_cli():
    print("🤖 Tina AI Terminal Mode")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You > ")

        if user_input.lower() in ["exit", "quit"]:
            print("Tina > Goodbye!")
            break

        intent = classify_intent(user_input)

        if intent == "coding":
            response = coding.handle(user_input)
        elif intent == "knowledge":
            response = knowledge.handle(user_input)
        else:
            response = conversation.handle(user_input)

        print(f"Tina ({intent}) > {response}\n")

if __name__ == "__main__":
    run_cli()
