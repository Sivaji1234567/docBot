<h1 align="center">🤖 DocBot — Company Document Chatbot</h1>

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-blueviolet?logo=chainlink&logoColor=white)](https://python.langchain.com/docs/introduction/)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?logo=ollama&logoColor=white)](https://ollama.com/library)
![License](https://img.shields.io/badge/License-MIT-green)

<p align="center">
  <strong>A fully local, privacy-first RAG chatbot for company policy and HR documents — no paid APIs, no data leaving your machine.</strong>
</p>

---

## 📌 Overview

**DocBot** is a production-ready, locally-hosted Retrieval-Augmented Generation (RAG) chatbot that lets employees instantly query internal company documents — HR policies, travel guidelines, leave rules, and more — using natural language.

Built with **FastAPI**, **LangChain**, **ChromaDB**, and **Ollama**, it runs entirely on your own hardware with no external API calls.

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🔒 **100% Local & Private** | All inference runs on your machine via Ollama — zero data sent externally |
| 📄 **Multi-format Support** | Ingest PDF, DOCX, and TXT documents out of the box |
| ⚡ **Fast Vector Search** | ChromaDB-backed semantic search for relevant document chunks |
| 🧠 **LangChain RAG Pipeline** | Accurate, context-grounded answers with source attribution |
| 🌐 **REST API** | Clean FastAPI endpoints with auto-generated Swagger UI |
| 🔧 **Fully Configurable** | All model, chunking, and path settings in a single `config.py` |

---

## 🏗️ Tech Stack

```
Backend     → FastAPI (Python)
LLM         → Llama 3.2 via Ollama (local)
Embeddings  → nomic-embed-text via Ollama (local)
Vector DB   → ChromaDB (persistent)
RAG Chain   → LangChain
Doc Parsing → PDF, DOCX, TXT support
```

---

## 🚀 Quick Start

### 1. Prerequisites

- [Ollama](https://ollama.ai) installed and running
- Python 3.10+

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 2. Clone & Install

```bash
git clone <repo-url>
cd docbot
pip install -r requirements.txt
```

### 3. Add Your Documents

Drop PDF, DOCX, or TXT files into the `docs/` folder:

```bash
cp your-handbook.pdf docs/
cp leave-policy.docx docs/
cp travel-policy.txt docs/
```

### 4. Ingest Documents

```bash
python -m app.ingest
```

> Or trigger ingestion via the API after the server starts.

### 5. Start the Server

```bash
uvicorn main:app --reload
```

- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`

---

## 🔌 API Reference

### `GET /health` — Health Check
```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

### `POST /ingest` — Ingest Documents
```bash
curl -X POST http://localhost:8000/ingest
# {"status": "ok", "chunks_indexed": 42}
```

### `POST /chat` — Ask a Question
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many sick days do I get?"}'
```

**Response:**
```json
{
  "answer": "Employees receive 10 sick days per year.",
  "sources": ["docs/policy.txt"]
}
```

---

## ⚙️ Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `CHAT_MODEL` | `llama3.2` | Chat/completion model |
| `CHUNK_SIZE` | `500` | Characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `4` | Chunks retrieved per query |
| `CHROMA_PATH` | `./chroma_db` | ChromaDB persistence directory |
| `DOCS_PATH` | `./docs` | Source documents directory |

---

## 📁 Project Structure

```
docbot/
├── docs/               # Drop PDF/DOCX/TXT company files here
├── chroma_db/          # Auto-created by ingest (gitignored)
├── app/
│   ├── __init__.py
│   ├── ingest.py       # Load, chunk, embed & store docs
│   ├── retriever.py    # Vector search logic
│   ├── chain.py        # LangChain RAG chain setup
│   └── prompts.py      # System prompt templates
├── main.py             # FastAPI app entry point
├── config.py           # All settings
└── requirements.txt
```

---

## 🗺️ How It Works

```
User Question
     │
     ▼
[FastAPI /chat endpoint]
     │
     ▼
[Embed question with nomic-embed-text]
     │
     ▼
[ChromaDB semantic search → top-K chunks]
     │
     ▼
[LangChain RAG chain + Llama 3.2]
     │
     ▼
Answer + Source Attribution
```

---

## 🛣️ Roadmap

- [ ] Streaming responses via Server-Sent Events
- [ ] Multi-tenant document namespacing
- [ ] Web UI (React / Streamlit frontend)
- [ ] Docker Compose deployment
- [ ] Authentication & role-based access

---

## 📄 License

This project is licensed under the **MIT License**.

---

<p align="center">Built with ❤️ using FastAPI · LangChain · ChromaDB · Ollama</p>
