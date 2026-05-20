# experts/knowledge.py

from core.llm import llm
from core.personality import PERSONALITY_PROMPT

from memory.short_term import format_for_prompt


# =====================================================
# 🧠 KNOWLEDGE EXPERT
# =====================================================

async def handle(text: str):

    # =================================================
    # MEMORY CONTEXT
    # =================================================
    memory = format_for_prompt()

    # =================================================
    # KNOWLEDGE PROMPT
    # =================================================
    prompt = f"""
Conversation memory:
{memory}

User question:
{text}

Instructions:
- Answer clearly and accurately
- Keep responses concise but informative
- Be natural and conversational
- If unsure, say so honestly
"""

    # =================================================
    # LLM RESPONSE
    # =================================================
    reply = llm.chat(
        user_prompt=prompt,
        system_prompt=PERSONALITY_PROMPT,
        temperature=0.3,
        max_tokens=250
    )

    # =================================================
    # STRUCTURED RESPONSE
    # =================================================
    return {
        "type": "chat",
        "reply": reply
    }