from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mosaicml/mpt-7b-chat"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    device_map="auto",  # automatically chooses GPU/CPU
    torch_dtype="auto"  # automatically chooses float16 if GPU supports
)
