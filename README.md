# Docbot — Company Document Chatbot

A fully local RAG chatbot for company policy and HR documents. No paid APIs required.

## Prerequisites

1. [Ollama](https://ollama.ai) installed and running.
2. Pull the required models:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3.2
   ```
3. Python 3.10+

## Setup

```bash
git clone <repo-url>
cd docbot
pip install -r requirements.txt
```

## Add Documents

Drop PDF, DOCX, or TXT files into the `docs/` folder:

```bash
cp your-handbook.pdf docs/
cp leave-policy.docx docs/
cp travel-policy.txt docs/
```

## Ingest Documents

Run ingestion from the command line:

```bash
python -m app.ingest
```

Or trigger it via the API after the server is running (see below).

## Run the Server

```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

## API Examples

### Check server health

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### Ingest documents

```bash
curl -X POST http://localhost:8000/ingest
```

Response:
```json
{"status": "ok", "chunks_indexed": 42}
```

### Ask a question

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "how many sick days do I get?"}'
```

Response:
```json
{
  "answer": "Employees receive 10 sick days per year.",
  "sources": ["docs/policy.txt"]
}
```

## Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `CHAT_MODEL` | `llama3.2` | Chat/completion model |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `4` | Chunks retrieved per query |
| `CHROMA_PATH` | `./chroma_db` | ChromaDB persistence directory |
| `DOCS_PATH` | `./docs` | Source documents directory |

## Project Structure

```
docbot/
├── docs/           # Drop PDF/DOCX/TXT company files here
├── chroma_db/      # Auto-created by ingest (gitignored)
├── app/
│   ├── __init__.py
│   ├── ingest.py   # Load, chunk, embed, store docs
│   ├── retriever.py# Vector search logic
│   ├── chain.py    # LangChain RAG chain setup
│   └── prompts.py  # System prompt templates
├── main.py         # FastAPI app
├── config.py       # All settings
└── requirements.txt
```
