# main.py

import logging
import asyncio
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.router import classify_intent
from experts import conversation, coding, knowledge, action, hacking

logger = logging.getLogger("Tina")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Tina",
    description="Personal AI Assistant",
    version="1.1"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Map intents to their respective handlers
INTENT_HANDLERS = {
    "coding": coding.handle,
    "knowledge": knowledge.handle,
    "conversation": conversation.handle,
    "action": action.handle,
    "hacking": hacking.handle,
}


@app.get("/", response_model=dict)
async def root() -> dict:
    """Root endpoint to check if Tina is running."""
    return {"message": "Tina is up and running!"}


@app.get("/ask", response_model=dict)
async def ask(q: str = Query(..., description="Ask Tina something")) -> dict:
    """
    Main endpoint for asking Tina a question.
    Routes the question to the appropriate expert based on intent.
    """
    try:
        logger.info(f"Received question: {q}")

        # Classify intent
        intent = classify_intent(q)
        logger.info(f"Detected intent: {intent}")

        # Get the appropriate handler; default to conversation
        handler = INTENT_HANDLERS.get(intent, conversation.handle)

        # Call async or sync handler appropriately
        if asyncio.iscoroutinefunction(handler):
            response = await handler(q)
        else:
            # Run synchronous handlers in a background thread to avoid blocking
            response = await asyncio.to_thread(handler, q)

        return {"intent": intent, "response": response}

    except Exception as e:
        logger.error(f"Error handling question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
