from core.llm import llm
from core.personality import PERSONALITY_PROMPT


def handle(text: str):

    try:
        # ==========================
        # PURE CHAT EXPERT
        # ==========================

        reply = llm.chat(
            user_prompt=text,
            system_prompt=PERSONALITY_PROMPT,
            temperature=0.3,
            max_tokens=300
        )

        # ==========================
        # RETURN STRUCTURED OUTPUT
        # ==========================
        return {
            "type": "chat",
            "reply": reply.strip()
        }

    except Exception as e:
        return {
            "type": "chat",
            "reply": "I had trouble responding to that."
        }