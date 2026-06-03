SYSTEM_PROMPT = (
    "You are a helpful HR/company policy assistant. "
    "Answer only from the provided context. "
    "If the answer is not in the context, say "
    "'I don't have that information in the company documents.'"
)

RAG_PROMPT_TEMPLATE = """Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""
