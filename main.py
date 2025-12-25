# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from experts.conversation import handle  # Import the updated handle function

app = FastAPI(
    title="Tina AI",
    description="Personal AI Assistant",
    version="1.0"
)

# Optional: Allow CORS if testing from a browser/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """
    Root endpoint to check if the server is running
    """
    return {"message": "Tina AI is running!"}

@app.get("/ask")
def ask(q: str = Query(..., description="Your question or input to Tina AI")):
    """
    Endpoint to process user input via conversation expert.
    """
    try:
        # Use the updated handle function from conversation.py
        response = handle(q)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
