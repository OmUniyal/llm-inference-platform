"""
RAG API — FastAPI service.

Exposes RAGChain as a REST API, running on nitro-server.
Same RAG logic as the Gradio app, served as a production HTTP API.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.generation.rag_chain import RAGChain
from src.utils.logger import logger

app = FastAPI(
    title="RAG Document Q&A API",
    description="Self-hosted RAG API running on nitro-server, backed by Ollama (phi3:mini).",
    version="1.0.0",
)

# Initialize once at startup — avoids reloading embedder/LLM client per request
rag_chain: RAGChain | None = None


@app.on_event("startup")
def startup_event():
    global rag_chain
    logger.info("Initializing RAG chain...")
    rag_chain = RAGChain()
    logger.info("RAG chain ready.")


class QueryRequest(BaseModel):
    question: str
    top_k: int | None = None


class SourceItem(BaseModel):
    source: str
    page: int
    score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceItem]
    chunks_used: int


@app.get("/health")
def health_check():
    """Basic health check — used by Docker healthcheck and monitoring."""
    return {"status": "ok", "rag_ready": rag_chain is not None}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Ask a question against the ingested documents.
    Returns the answer plus source attribution.
    """
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG chain not initialized yet")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = rag_chain.query(request.question, top_k=request.top_k)
        return result
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "service": "RAG Document Q&A API",
        "status": "running",
        "docs": "/docs",
    }