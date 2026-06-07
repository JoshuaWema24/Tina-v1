from core.router import route
from core.personality import PERSONALITY_PROMPT
from core.llm import llm

from memory.short_term import add, get_recent_context
from memory.retrieval import build_memory_context
from tools.executor import execute

import asyncio
import logging

logger = logging.getLogger("Tina")


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
    memory_context,
    conversation_history,
    tool_reply=""
):

    try:

        combined = "\n".join(expert_outputs)

        memory_block = format_memory_block(memory_context)

        history_block = conversation_history if conversation_history else "No prior conversation."

        tool_block = (
            f"\n========================\nTOOL RESULT\n========================\n{tool_reply}"
            if tool_reply else ""
        )

        prompt = f"""
You are Tina, a persistent cognitive assistant.

========================
CONVERSATION HISTORY
========================
{history_block}

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
{tool_block}

========================
COGNITIVE INSTRUCTIONS
========================
- You are a single unified intelligence
- ALWAYS use conversation history to maintain full context across turns
- Never lose track of ongoing topics like projects, tasks, or previous requests
- If the user references something said earlier (e.g. "that project", "continue", "yes"), resolve it from history
- If a TOOL RESULT is present, confirm the action naturally (e.g. "Chrome is open!") — do NOT say you will do it, it's already done
- Use memory as background knowledge only
- Never mention internal systems, experts, or routing to the user
- Be natural, calm, and intelligent
- Prioritize correctness over creativity
- If memory conflicts with input, clarify gently
- Keep response concise but meaningful

FINAL TASK:
Generate ONE coherent, context-aware response.
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
        # 1. PULL CONVERSATION HISTORY (ALWAYS)
        # =================================================
        conversation_history = get_recent_context(limit=6)

        # =================================================
        # 2. MEMORY CONTEXT (ALWAYS ATTEMPT, NEVER GATE)
        # =================================================
        memory_context = ""

        try:
            memory_context = build_memory_context(text)
        except Exception as e:
            logger.warning(f"Memory retrieval skipped: {e}")

        # =================================================
        # 3. RUN EXPERT SYSTEMS
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
        # 4. EXTRACT OUTPUTS + EXECUTE TOOLS
        # =================================================
        replies = []
        collected_data = []
        final_type = "chat"
        tool_reply = ""

        for r in expert_results:

            if r.get("reply"):
                replies.append(r["reply"])

            if r.get("data"):
                collected_data.append(r["data"])

            if r.get("type") == "action":
                final_type = "action"
                tool_name = r.get("tool")

                if tool_name:
                    logger.info(f"Dispatching tool: {tool_name}")
                    tool_result = execute(tool_name)

                    if tool_result["success"]:
                        tool_reply = (
                            tool_result["message"]
                            or f"Done — {tool_name.replace('_', ' ')} launched."
                        )
                        logger.info(f"Tool succeeded: {tool_name}")
                    else:
                        tool_reply = f"I tried to {tool_name.replace('_', ' ')} but something went wrong: {tool_result['message']}"
                        logger.warning(f"Tool failed: {tool_name} — {tool_result['message']}")

        # =================================================
        # 5. MEMORY-AWARE FUSION (NOW WITH HISTORY)
        # =================================================
        final_reply = await unify_response(
            user_input=text,
            intents=intents,
            expert_outputs=replies,
            memory_context=memory_context,
            conversation_history=conversation_history,
            tool_reply=tool_reply
        )

        # =================================================
        # 6. MEMORY WRITE-BACK
        # =================================================
        add(text, final_reply)

        # =================================================
        # 7. RETURN CONTRACT
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