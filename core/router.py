# core/router.py

from core.intent import classify_intents

from experts import (
    conversation,
    action,
    coding,
    knowledge,
    security
)

# =====================================================
# 🧠 EXPERT MAP
# =====================================================

EXPERT_MAP = {
    "conversation": conversation,
    "action": action,
    "coding": coding,
    "knowledge": knowledge,
    "security": security,

    # temporary emotion handling
    # later you'll create emotion.py
    "emotion": conversation
}

# =====================================================
# 🧠 ROUTER
# =====================================================

def route(text: str):

    # ================================================
    # DETECT MULTIPLE INTENTS
    # ================================================
    intents = classify_intents(text)

    experts = []

    # ================================================
    # MAP INTENTS → EXPERTS
    # ================================================
    for intent in intents:

        expert = EXPERT_MAP.get(intent)

        # avoid duplicate experts
        if expert and expert not in experts:
            experts.append(expert)

    # ================================================
    # SAFETY FALLBACK
    # ================================================
    if not experts:
        experts.append(conversation)
        intents = ["conversation"]

    # ================================================
    # FINAL ROUTING OBJECT
    # ================================================
    return {
        "intents": intents,
        "experts": experts
    }