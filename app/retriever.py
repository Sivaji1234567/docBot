from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

import config


def get_retriever():
    """Return a ChromaDB retriever configured from config.py."""
    embeddings = OllamaEmbeddings(
        model=config.EMBED_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )
    vectorstore = Chroma(
        persist_directory=config.CHROMA_PATH,
        embedding_function=embeddings,
    )
    return vectorstore.as_retriever(search_kwargs={"k": config.TOP_K})
