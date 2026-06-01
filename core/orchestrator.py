from core.router import route
from core.personality import PERSONALITY_PROMPT
from core.llm import llm

from memory.short_term import add
from memory.retrieval import build_memory_context

import asyncio
import logging

logger = logging.getLogger("Tina")


# =====================================================
# 🧠 MEMORY USAGE GATE (IMPORTANT)
# =====================================================

def should_use_memory(text: str) -> bool:

    keywords = [
        "remember",
        "we talked",
        "last time",
        "before",
        "earlier",
        "continue",
        "project",
        "update",
        "again",
        "that"
    ]

    text = text.lower()

    return any(k in text for k in keywords)


# =====================================================
# 🧠 MEMORY FORMATTER (STRUCTURED CONTEXT)
# =====================================================

def format_memory_block(memory_context: str) -> str:

    if not memory_context:
        return ""

    return f"""
[LONG_TERM_MEMORY]
{memory_context}

[MEMORY_RULES]
- Use memory only if relevant
- Do not assume memory is always correct
- Resolve contradictions using latest user input
- Ignore memory if unrelated
"""


# =====================================================
# 🧠 RESPONSE UNIFIER (COGNITIVE FUSION ENGINE)
# =====================================================

async def unify_response(
    user_input,
    intents,
    expert_outputs,
    memory_context
):

    try:

        combined = "\n".join(expert_outputs)

        memory_block = format_memory_block(memory_context)

        prompt = f"""
You are Tina, a persistent cognitive assistant.

========================
USER INPUT
========================
{user_input}

========================
INTENTS
========================
{", ".join(intents)}

========================
MEMORY CONTEXT
========================
{memory_block}

========================
EXPERT OUTPUTS
========================
{combined}

========================
COGNITIVE INSTRUCTIONS
========================
- You are a single unified intelligence
- Use memory as background knowledge only
- Never mention internal systems, experts, or routing
- Be natural, calm, and intelligent
- Prioritize correctness over creativity
- If memory conflicts with input, clarify gently
- Keep response concise but meaningful

FINAL TASK:
Generate ONE coherent response.
"""

        result = llm.chat(
            user_prompt=prompt,
            system_prompt=PERSONALITY_PROMPT,
            temperature=0.2,
            max_tokens=200
        )

        return result.strip() if result else "\n".join(expert_outputs)

    except Exception as e:

        logger.error(f"Unifier error: {e}", exc_info=True)

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
        # 1. MEMORY CONTEXT (GATED)
        # =================================================
        memory_context = ""

        if should_use_memory(text):
            memory_context = build_memory_context(text)

        # =================================================
        # 2. RUN EXPERT SYSTEMS
        # =================================================
        expert_results = []

        for expert in experts:

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
        # 3. EXTRACT OUTPUTS
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
        # 4. MEMORY-AWARE FUSION
        # =================================================
        final_reply = await unify_response(
            user_input=text,
            intents=intents,
            expert_outputs=replies,
            memory_context=memory_context
        )

        # =================================================
        # 5. MEMORY WRITE-BACK
        # =================================================
        add(text, final_reply)

        # =================================================
        # 6. RETURN CONTRACT
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