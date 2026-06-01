from core.router import route
from core.personality import PERSONALITY_PROMPT
from core.llm import llm

from memory.short_term import add
from memory.retrieval import build_memory_context

import asyncio
import logging

logger = logging.getLogger("Tina")


# =====================================================
# 🧠 RESPONSE UNIFIER (IMPROVED)
# =====================================================
async def unify_response(user_input, intents, expert_outputs, memory_context):

    try:

        combined = "\n".join(expert_outputs)

        prompt = f"""
You are Tina, a cognitive assistant.

USER INPUT:
{user_input}

INTENTS:
{", ".join(intents)}

MEMORY CONTEXT:
{memory_context}

EXPERT OUTPUTS:
{combined}

TASK:
Merge everything into ONE intelligent response.

RULES:
- Use memory when relevant
- Prioritize correctness over creativity
- Be natural and conversational
- Never mention experts
- Keep response concise but meaningful
- If memory contradicts input, clarify politely
"""

        return llm.chat(
            user_prompt=prompt,
            system_prompt=PERSONALITY_PROMPT,
            temperature=0.2,
            max_tokens=180
        ).strip()

    except Exception as e:

        logger.error(f"Unifier error: {e}", exc_info=True)
        return "\n".join(expert_outputs)


# =====================================================
# 🧠 MAIN ORCHESTRATOR (UPGRADED)
# =====================================================
async def process(text: str):

    routing = route(text)

    intents = routing["intents"]
    experts = routing["experts"]

    try:

        # =================================================
        # 0. MEMORY CONTEXT (NEW - CRITICAL)
        # =================================================
        memory_context = build_memory_context(text)

        # =================================================
        # 1. RUN EXPERTS WITH CONTEXT
        # =================================================
        expert_results = []

        for expert in experts:

            # inject memory context into expert if supported
            if hasattr(expert, "handle_with_context"):
                result = expert.handle_with_context(text, memory_context)
            else:
                result = expert.handle(text)

            if asyncio.iscoroutine(result):
                result = await result

            if isinstance(result, str):
                result = {
                    "type": "chat",
                    "reply": result
                }

            expert_results.append(result)

        # =================================================
        # 2. EXTRACT RESULTS
        # =================================================
        replies = []
        collected_data = []
        final_type = "chat"

        for r in expert_results:

            if r.get("reply"):
                replies.append(r["reply"])

            if r.get("data"):
                collected_data.append(r["data"])

            if r.get("type") == "action":
                final_type = "action"

        # =================================================
        # 3. UNIFY RESPONSE (NOW MEMORY-AWARE)
        # =================================================
        final_reply = await unify_response(
            user_input=text,
            intents=intents,
            expert_outputs=replies,
            memory_context=memory_context
        )

        # =================================================
        # 4. MEMORY STORAGE (SMARTER NOW)
        # =================================================
        add(text, final_reply)

        # =================================================
        # 5. RETURN CONTRACT
        # =================================================
        return {
            "intents": intents,
            "type": final_type,
            "reply": final_reply,
            "data": collected_data
        }

    except Exception as e:

        logger.error(f"Orchestrator error: {e}", exc_info=True)

        return {
            "intents": ["conversation"],
            "type": "chat",
            "reply": "Something went wrong while processing that."
        }