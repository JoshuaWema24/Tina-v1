# experts/conversation.py

import logging
import asyncio
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

logger = logging.getLogger("Tina")

MODEL_NAME = "microsoft/DialoGPT-small"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()
except Exception as e:
    tokenizer = None
    model = None
    logger.error(f"Failed to load DialoGPT: {e}", exc_info=True)

FALLBACK = "Hello! 😊 How can I help you today?"

# Hard blacklist to kill junk output
BAD_TOKENS = ["lol", "xd", "jk", "haha", "!!!", "???", "lmao"]


async def handle(text: str) -> str:
    if tokenizer is None or model is None:
        return FALLBACK

    text = text.strip()
    if not text:
        return FALLBACK

    try:
        # VERY IMPORTANT:
        # DialoGPT works best with JUST the user input
        input_ids = tokenizer.encode(
            text + tokenizer.eos_token,
            return_tensors="pt"
        )

        attention_mask = torch.ones_like(input_ids)

        output_ids = await asyncio.to_thread(
            model.generate,
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=40,       # SHORT answers
            do_sample=False,         # 🔥 NO SAMPLING
            num_beams=1,             # deterministic
            repetition_penalty=1.4,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(
            output_ids[0][input_ids.shape[-1]:],
            skip_special_tokens=True
        ).strip()

        # Hard cleanup
        response_lower = response.lower()
        if (
            not response
            or len(response) < 2
            or any(bad in response_lower for bad in BAD_TOKENS)
        ):
            return FALLBACK

        # Final clamp
        return response[:200]

    except Exception as e:
        logger.error(f"Conversation error: {e}", exc_info=True)
        return FALLBACK
