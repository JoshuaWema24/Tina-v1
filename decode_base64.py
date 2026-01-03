from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Define model and tokenizer name
model_name = "gpt2"  # You can use "distilgpt2" for a smaller model

# Download and cache the model & tokenizer
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Save locally so you can use offline later
model.save_pretrained('./gpt2')
tokenizer.save_pretrained('./gpt2')

print("Model and tokenizer have been downloaded and saved locally!")
