from core.router import classify_intent
from experts import conversation, action, coding, knowledge, hacking

def process_input(text: str):
    intent = classify_intent(text)

    if intent == "action":
        return action.handle(text)

    if intent == "coding":
        return coding.handle(text)
    
    if intent == "knowledge":
        return knowledge.handle(text)
    
    if intent == "hacking":
        return hacking.handle(text)

    return conversation.handle(text)
