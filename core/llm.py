# core/llm.py

from core.router import classify_intent
from experts import action, coding, knowledge, hacking, conversation

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
        from experts import knowledge 
        return knowledge.handle(text)
    
    if intent == "hacking":
        from experts import hacking
        return hacking.handle(text)

    # conversation
    from experts import conversation  
    return conversation.handle(text)
