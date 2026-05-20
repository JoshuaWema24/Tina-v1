# experts/action.py

import asyncio
import logging
import subprocess
from typing import Optional, Dict, Callable, Union
from pathlib import Path
from difflib import get_close_matches

logger = logging.getLogger("Tina")

# =====================================================
# 🖥️ COMMAND EXECUTION
# =====================================================

def _windows_command(cmd: Optional[str]) -> Optional[str]:
    if not cmd:
        return "Application not found."

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
        return result.stderr.strip()
    except Exception as e:
        logger.error(e)
        return str(e)


# =====================================================
# 🧠 ACTION HELPERS
# =====================================================

def find_chrome_path() -> Optional[str]:
    paths = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for path in paths:
        if path.exists():
            return str(path)
    return None


def open_screenshots_folder() -> Optional[str]:
    path = Path.home() / "Pictures" / "Screenshots"
    if path.exists():
        return _windows_command(f'explorer "{path}"')
    return "Screenshots folder not found."


# =====================================================
# 🧠 SAFE ACTIONS
# =====================================================

ActionFunc = Callable[[], Optional[str]]

SAFE_ACTIONS: Dict[str, Dict[str, object]] = {

    "notepad": {
        "func": lambda: _windows_command("notepad"),
        "keywords": ["notepad", "notes", "text editor"]
    },
    "calculator": {
        "func": lambda: _windows_command("calc"),
        "keywords": ["calculator", "calc", "math"]
    },
    "chrome": {
        "func": lambda: _windows_command(find_chrome_path()),
        "keywords": ["chrome", "browser", "google"]
    },
    "paint": {
        "func": lambda: _windows_command("mspaint"),
        "keywords": ["paint", "drawing"]
    },
    "screenshot": {
        "func": lambda: _windows_command("explorer ms-screenclip:"),
        "keywords": ["screenshot", "screen shot", "capture screen", "snipping tool"]
    },
    "screen_record": {
        "func": lambda: _windows_command("explorer ms-gamingoverlay:"),
        "keywords": ["screen record", "record screen", "screen recording"]
    },
    "screenshots_folder": {
        "func": open_screenshots_folder,
        "keywords": ["open screenshots", "screenshots folder"]
    },
}

ACTION_VERBS = {"open", "launch", "start", "run", "take", "record", "capture"}


# =====================================================
# 🔍 FUZZY MATCHING
# =====================================================

def fuzzy_match(text: str, options: list[str], cutoff: float = 0.6) -> Optional[str]:
    matches = get_close_matches(text, options, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def extract_action(text: str) -> Optional[str]:
    keyword_map = {}
    for action, info in SAFE_ACTIONS.items():
        for kw in info["keywords"]:
            keyword_map[kw] = action

    full_match = fuzzy_match(text, list(keyword_map.keys()))
    if full_match:
        return keyword_map[full_match]

    for word in text.split():
        match = fuzzy_match(word, list(keyword_map.keys()))
        if match:
            return keyword_map[match]

    return None


# =====================================================
# 🧠 JSON ACTION HANDLER (IMPROVED)
# =====================================================

def match_app(app: str) -> Optional[str]:
    """
    Stronger matching for AI-provided app names
    """
    app = app.lower()

    for key, info in SAFE_ACTIONS.items():
        if app == key:
            return key

        if app in info["keywords"]:
            return key

        if app in " ".join(info["keywords"]):
            return key

    return None


def handle_json_action(data: dict) -> Optional[str]:
    action = data.get("action")
    app = data.get("app")

    logger.info(f"AI Action received: {data}")

    if not action:
        return None

    if action == "open_app" and app:
        matched = match_app(app)

        if matched:
            result = SAFE_ACTIONS[matched]["func"]()
            return result or f"Opened {matched}"

        return f"I don't know how to open {app} yet."

    return None


# =====================================================
# 🚀 MAIN HANDLER
# =====================================================

async def handle(input_data: Union[str, dict]) -> str:
    try:
        # ==========================
        # 1. JSON (AI-driven)
        # ==========================
        if isinstance(input_data, dict):
            result = await asyncio.to_thread(handle_json_action, input_data)

            if result:
                return f"✅ {result}"

            return "❌ I couldn't execute that action."

        # ==========================
        # 2. TEXT FALLBACK
        # ==========================
        text = input_data.lower().strip()

        if not any(verb in text for verb in ACTION_VERBS):
            return "🤔 I didn’t detect a system action."

        action = extract_action(text)
        if not action:
            return "❌ I couldn't understand which action to perform."

        logger.info(f"Fallback action detected: {action}")

        result = await asyncio.to_thread(SAFE_ACTIONS[action]["func"])

        if result:
            return f"✅ {action.replace('_', ' ').title()}: {result}"

        return f"✅ {action.replace('_', ' ').title()} executed."

    except Exception as e:
        logger.error(f"Action error: {e}", exc_info=True)
        return "⚠️ Something went wrong while performing the action."