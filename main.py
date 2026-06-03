from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.chain import build_chain
from app.ingest import ingest_documents

app = FastAPI(title="Docbot - Company Document Chatbot")

# Chain and retriever are built lazily on first /chat request
_chain = None
_retriever = None


def get_chain():
    global _chain, _retriever
    if _chain is None:
        _chain, _retriever = build_chain()
    return _chain, _retriever


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest():
    global _chain, _retriever
    try:
        chunks = ingest_documents()
        _chain = None  # Reset so next /chat reloads the updated vectorstore
        _retriever = None
        return IngestResponse(status="ok", chunks_indexed=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        chain, retriever = get_chain()
        answer = chain.invoke({"question": request.question})
        source_docs = retriever.invoke(request.question)
        sources = [doc.metadata.get("source", "unknown") for doc in source_docs]
        return ChatResponse(answer=answer, sources=list(set(sources)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
