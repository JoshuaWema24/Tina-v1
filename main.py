# main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from core.router import classify_intent
from experts import conversation, coding, knowledge

app = FastAPI(
    title="Tina",
    description="Personal AI Assistant",
    version="1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Tina is up and running!"}

@app.get("/ask")
def ask(q: str = Query(..., description="Ask Tina something")):
    try:
        intent = classify_intent(q)

        if intent == "coding":
            response = coding.handle(q)
        elif intent == "knowledge":
            response = knowledge.handle(q)
        else:
            response = conversation.handle(q)

        return {
            "intent": intent,
            "response": response
        }

    except Exception as e:
        return {"error": str(e)}
