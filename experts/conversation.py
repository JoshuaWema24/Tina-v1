from transformers import pipeline

# Load model ONCE at startup
try:
    conversation_model = pipeline(
        "text-generation",
        model="gpt2"  # Using the full GPT-2 model
    )
except Exception as e:
    conversation_model = None
    print("⚠️ Failed to load conversation model:", e)


def handle(text: str) -> str:
    """
    Handles conversation-related queries using a local language model.
    """

    if conversation_model is None:
        return "Sorry, my conversation module is not available right now."

    # Simple, controlled prompt
    prompt = (
        "You are Tina, a friendly and helpful AI assistant.\n"
        f"User: {text}\n"
        "Tina:"
    )

    try:
        output = conversation_model(
            prompt,
            max_length=120,  
            max_new_tokens=256,  
            truncation=True, 
            do_sample=True,
            temperature=0.7,
            num_return_sequences=1
        )

        generated_text = output[0]["generated_text"]

        # Extract only Tina's reply
        response = generated_text.split("Tina:")[-1].strip()

        return response if response else "I’m not sure how to respond to that."

    except Exception as e:
        print("⚠️ Conversation error:", e)
        return "Something went wrong while thinking."
