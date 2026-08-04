from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.agent_with_narrative import run_agent


app = FastAPI(
    title="AI Agent API",
    version="0.1.0",
)

STATIC_DIR = Path(__file__).parent / "static"


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root() -> FileResponse:
    """
    Serve the browser-based chat interface.
    """

    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """
    Return a simple health check.
    """

    return {
        "status": "healthy",
        "service": "ai-agent",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a user message to the AI agent and return its answer.
    """

    answer = run_agent(request.message)

    return ChatResponse(answer=answer)