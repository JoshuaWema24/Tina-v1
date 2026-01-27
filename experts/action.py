# experts/action.py

import asyncio
import logging
import os
import platform

logger = logging.getLogger("Tina")

SAFE_ACTIONS = {
    "open notepad": lambda: os.system("notepad") if platform.system() == "Windows" else "Not supported on this OS",
    "open calculator": lambda: os.system("calc") if platform.system() == "Windows" else "Not supported on this OS",
    "show files": lambda: os.listdir("."),
    
}


async def handle(text: str) -> str:
    """
    Handles 'action' intents. Executes safe system actions asynchronously.
    """
    text = text.lower().strip()

    try:
        
        for action, func in SAFE_ACTIONS.items():
            if action in text:
                
                result = await asyncio.to_thread(func)
                return f"✅ Action executed: {action}" if result is None else f"✅ Action result: {result}"

       
        return "I understand you want to do something, but I cannot perform that action right now."

    except Exception as e:
        logger.error(f"⚠️ Action error: {e}", exc_info=True)
        return "Something went wrong while performing the action."
