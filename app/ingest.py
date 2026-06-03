from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

import config


def load_documents(docs_path: str) -> list:
    """Load all PDF, DOCX, and TXT files from the given directory."""
    docs = []
    path = Path(docs_path)
    for file in path.iterdir():
        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
            docs.extend(loader.load())
        elif file.suffix.lower() == ".docx":
            loader = Docx2txtLoader(str(file))
            docs.extend(loader.load())
        elif file.suffix.lower() == ".txt":
            loader = TextLoader(str(file), encoding="utf-8")
            docs.extend(loader.load())
    return docs


def ingest_documents() -> int:
    """Load, chunk, embed, and persist documents. Returns number of chunks indexed."""
    print(f"Loading documents from {config.DOCS_PATH}...")
    documents = load_documents(config.DOCS_PATH)

    if not documents:
        print("No documents found.")
        return 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = OllamaEmbeddings(
        model=config.EMBED_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    print("Embedding and storing in ChromaDB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_PATH,
    )

    print(f"Indexed {len(chunks)} chunks successfully.")
    return len(chunks)


if __name__ == "__main__":
    ingest_documents()
