# core/llm.py

from core.router import classify_intent
from experts import action, coding  # conversation and knowledge imported locally

def call_llm(prompt: str) -> str:
    """
    Calls the LLM and returns the response.
    Replace this with your actual LLM call logic.
    """
    return f"LLM response: {prompt}"

def process_input(text: str) -> str:
    """
    Routes user input to the correct expert module based on intent.
    """
    intent = classify_intent(text)

    if intent == "action":
        return action.handle(text)

    if intent == "coding":
        return coding.handle(text)

    if intent == "knowledge":
        from experts import knowledge  # local import to avoid circular import
        return knowledge.handle(text)

    # conversation
    from experts import conversation  # local import to avoid circular import
    return conversation.handle(text)
