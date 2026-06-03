from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import config
from app.prompts import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE
from app.retriever import get_retriever


def build_chain() -> RetrievalQA:
    """Assemble and return the LangChain RetrievalQA chain."""
    llm = OllamaLLM(
        model=config.CHAT_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=f"{SYSTEM_PROMPT}\n\n{RAG_PROMPT_TEMPLATE}",
    )

    retriever = get_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain
