# download_phi2.py
"""
Download and cache the Phi-2-small model locally for Tina.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import os

MODEL_NAME = "stabilityai/phi-2-small"
LOCAL_DIR = "models/phi2-small"  # You can change this path

os.makedirs(LOCAL_DIR, exist_ok=True)

print(f"Downloading tokenizer for {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=LOCAL_DIR)

print(f"Downloading model for {MODEL_NAME}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=LOCAL_DIR)

print(f"Model and tokenizer saved locally at {LOCAL_DIR}")
print("✅ Phi-2-small is ready to use!")
