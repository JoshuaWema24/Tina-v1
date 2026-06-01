# experts/action.py

import logging
from difflib import get_close_matches

logger = logging.getLogger("Tina")

# =====================================================
# TOOL MAP
# =====================================================

ACTION_MAP = {

    "open_chrome": [
        "chrome",
        "google chrome",
        "browser",
        "google"
    ],

    "open_calculator": [
        "calculator",
        "calc",
        "math"
    ],

    "open_notepad": [
        "notepad",
        "notes",
        "text editor"
    ],

    "open_paint": [
        "paint",
        "drawing",
        "mspaint"
    ],

    "open_screenshot_tool": [
        "screenshot",
        "screen shot",
        "capture screen",
        "snipping tool"
    ],

    "open_screen_recording": [
        "screen record",
        "record screen",
        "screen recording"
    ],

    "open_screenshots_folder": [
        "screenshots folder",
        "open screenshots",
        "saved screenshots"
    ],

    "open_vscode": [
    "vscode",
    "vs code",
    "visual studio code",
    "code editor",
    "editor"
],

"open_explorer": [
    "file explorer",
    "explorer",
    "files",
    "folder",
    "windows explorer"
]
}

# =====================================================
# ACTION VERBS
# =====================================================

ACTION_VERBS = {
    "open",
    "launch",
    "start",
    "run",
    "take",
    "capture",
    "record"
}


# =====================================================
# FUZZY MATCH
# =====================================================

def fuzzy_match(text, choices, cutoff=0.8):

    matches = get_close_matches(
        text,
        choices,
        n=1,
        cutoff=cutoff
    )

    return matches[0] if matches else None


# =====================================================
# FIND TOOL
# =====================================================

def detect_tool(text: str):

    text = text.lower().strip()

    # ---------------------------------
    # Exact match first
    # ---------------------------------

    for tool, keywords in ACTION_MAP.items():

        for keyword in keywords:

            if keyword in text:
                return tool

    # ---------------------------------
    # Fuzzy fallback
    # ---------------------------------

    all_keywords = []

    keyword_to_tool = {}

    for tool, keywords in ACTION_MAP.items():

        for keyword in keywords:

            all_keywords.append(keyword)

            keyword_to_tool[keyword] = tool

    match = fuzzy_match(
        text,
        all_keywords
    )

    if match:

        return keyword_to_tool[match]

    return None


# =====================================================
# MAIN HANDLER
# =====================================================

async def handle(user_input: str):

    text = user_input.lower().strip()

    # ---------------------------------
    # Verify action intent
    # ---------------------------------

    if not any(
        verb in text
        for verb in ACTION_VERBS
    ):
        return {
            "type": "chat",
            "reply": "No action detected."
        }

    # ---------------------------------
    # Find tool
    # ---------------------------------

    tool = detect_tool(text)

    if not tool:

        return {
            "type": "chat",
            "reply": (
                "I couldn't determine "
                "which action to perform."
            )
        }

    logger.info(
        f"Action Expert selected tool: {tool}"
    )

    # ---------------------------------
    # Return action request
    # ---------------------------------

    return {
        "type": "action",
        "tool": tool,
        "reply": ""
    }