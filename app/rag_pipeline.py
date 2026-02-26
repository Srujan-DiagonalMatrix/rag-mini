##############################################
# Q&A script.
##############################################

from ingestion import runIngestion
from langchain_core.documents import Document
import requests

# ✅ Must be a real Ollama LLM model, NOT "ollama"
# Example: "llama3" (change to what you have pulled)
llm_model = "nomic-embed-text"

ollama_base_url = "http://localhost:11434"


def loadRetriever(persistant_path: str = "./vector_db"):
    store = runIngestion(persist_path=persistant_path)
    retriever = store.as_retriever(search_kwargs={"k": 4})
    return retriever


def _format_context(docs: list[Document]) -> str:
    parts = []
    for i, d in enumerate(docs, start=1):
        text = (d.page_content or "").strip()
        if not text:
            continue
        parts.append(f"[Chunk {i}]\n{text}")
    return "\n\n".join(parts)


def _call_ollama_llm(prompt: str) -> str:
    url = f"{ollama_base_url}/v1/chat/completions"
    payload = {
        "model": llm_model,   # e.g. "llama3"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url=url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def answer(question: str, persistant_path: str = "./vector_db") -> str:
    retriever = loadRetriever(persistant_path=persistant_path)

    # ✅ DO NOT call _get_relevant_documents (internal API)
    try:
        docs = retriever.invoke(question)  # new LangChain versions
    except AttributeError:
        docs = retriever.get_relevant_documents(question)  # older versions

    context = _format_context(docs=docs)

    prompt = f"""
You are a helpful assistant.
Answer the user's question using ONLY the provided context.
If the answer is not in the context, say: "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""".strip()

    return _call_ollama_llm(prompt=prompt)


if __name__ == "__main__":
    question = "What is this document is all about?"
    print(answer(question=question))