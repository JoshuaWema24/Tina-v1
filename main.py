# main.py

import logging
import io

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from core.orchestrator import process
from core.llm import llm

# -------------------------------------------------
# LOGGING
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("Tina")

# -------------------------------------------------
# FASTAPI APP
# -------------------------------------------------
app = FastAPI(
    title="Tina",
    description="Personal AI Assistant Backend (Jarvis Architecture)",
    version="2.0"
)

# -------------------------------------------------
# CORS (Mobile / Desktop / Web)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# STARTUP EVENT
# -------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("🧠 Starting Tina core system...")

    llm.load()
    llm.chat("warmup")

    logger.info("✅ Tina is online and ready")

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Tina is running 🚀"
    }

# -------------------------------------------------
# MAIN CHAT ENDPOINT (UNIFIED BRAIN)
# -------------------------------------------------
@app.get("/ask")
async def ask(q: str = Query(..., description="Ask Tina something")):
    try:
        logger.info(f"📨 User query: {q}")

        # ==========================
        # 🧠 CORE ORCHESTRATOR (BRAIN)
        # ==========================
        result = await process(q)

        # ==========================
        # NORMALIZE RESPONSE
        # ==========================
        if not isinstance(result, dict):
            return {
                "intent": "unknown",
                "response": str(result)
            }

        # ==========================
        # ACTION RESPONSE (optional future use)
        # ==========================
        if result.get("type") == "action":
            return {
                "intent": result.get("intent"),
                "type": "action",
                "response": result.get("reply"),
                "data": result.get("data")
            }

        # ==========================
        # CHAT RESPONSE
        # ==========================
        return {
            "intent": result.get("intent", "conversation"),
            "type": result.get("type", "chat"),
            "response": result.get("reply", "I'm here."),
            "data": result.get("data")
        }

    except Exception as e:
        logger.error("❌ Tina API Error", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail="Tina encountered an internal error."
        )