# core/orchestrator.py

from core.router import route
from core.personality import PERSONALITY_PROMPT

from memory.short_term import add

from core.llm import llm

import asyncio
import logging

logger = logging.getLogger("Tina")


# =====================================================
# 🧠 RESPONSE UNIFIER
# =====================================================

async def unify_response(
    user_input: str,
    intents: list,
    expert_outputs: list
) -> str:

    try:

        combined = "\n".join(expert_outputs)

        prompt = f"""
User said:
{user_input}

Detected intents:
{", ".join(intents)}

Expert outputs:
{combined}

Rewrite this into ONE unified Tina response.

RULES:
- Sound natural and intelligent
- Keep responses smooth and conversational
- Never mention experts
- Never sound robotic
- Preserve important meaning
- Merge everything into ONE response
- If actions occurred, acknowledge them naturally
- Keep Tina's personality consistent
"""

        result = llm.chat(
            user_prompt=prompt,
            system_prompt=PERSONALITY_PROMPT,
            temperature=0.2,
            max_tokens=120
        )

        if result:
            return result.strip()

        return combined

    except Exception as e:

        logger.error(
            f"Response unifier error: {e}",
            exc_info=True
        )

        return "\n".join(expert_outputs)


# =====================================================
# 🧠 MAIN ORCHESTRATOR
# =====================================================

async def process(text: str):

    routing = route(text)

    intents = routing["intents"]
    experts = routing["experts"]

    try:

        # =================================================
        # 1. RUN ALL EXPERTS
        # =================================================

        expert_results = []

        for expert in experts:

            result = expert.handle(text)

            # async-safe
            if asyncio.iscoroutine(result):
                result = await result

            # normalize
            if isinstance(result, str):

                result = {
                    "type": "chat",
                    "reply": result
                }

            expert_results.append(result)

        # =================================================
        # 2. EXTRACT OUTPUTS
        # =================================================

        replies = []
        collected_data = []

        final_type = "chat"

        for result in expert_results:

            reply = result.get("reply", "")

            if reply:
                replies.append(reply)

            if result.get("data"):
                collected_data.append(result.get("data"))

            # if ANY expert is action → final type becomes action
            if result.get("type") == "action":
                final_type = "action"

        # =================================================
        # 3. UNIFY RESPONSES
        # =================================================

        final_reply = await unify_response(
            user_input=text,
            intents=intents,
            expert_outputs=replies
        )

        # =================================================
        # 4. MEMORY STORAGE
        # =================================================

        add(text, final_reply)

        # =================================================
        # 5. FINAL RESPONSE CONTRACT
        # =================================================

        return {
            "intents": intents,
            "type": final_type,
            "reply": final_reply,
            "data": collected_data
        }

    except Exception as e:

        logger.error(
            f"Orchestrator error: {e}",
            exc_info=True
        )

        return {
            "intents": ["conversation"],
            "type": "chat",
            "reply": (
                "Something went wrong while "
                "processing that."
            )
        }