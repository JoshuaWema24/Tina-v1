# experts/conversation.py
from transformers import pipeline

def handle(text: str) -> str:
    """
    Handles conversation-related queries using a pre-trained language model.
    """
    # Load the conversation model using Hugging Face Transformers (DistilGPT-2)
    conversation_model = pipeline("text-generation", model="distilgpt2")
    
    prompt = f"Have a friendly conversation with:\n{text}"
    
    # Generate a response based on the prompt
    responses = conversation_model(prompt, max_length=100, num_return_sequences=1)
    
    # Return the generated response (remove the prompt part)
    return responses[0]["generated_text"].replace(prompt, "").strip()
