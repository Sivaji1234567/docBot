from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import config
from app.prompts import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE
from app.retriever import get_retriever


def _format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain():
    """Assemble and return a LangChain LCEL RAG chain."""
    llm = OllamaLLM(
        model=config.CHAT_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=f"{SYSTEM_PROMPT}\n\n{RAG_PROMPT_TEMPLATE}",
    )

    retriever = get_retriever()

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: _format_docs(retriever.invoke(x["question"])),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever
