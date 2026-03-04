from __future__ import annotations

from typing import Optional, List, Any
from langchain_core.documents import Document
from dataclasses import dataclass
from app.embeddings import get_embeding_model
from app.vectorstore import VectorStoreManager
from app.ingestion import runIngestion

@dataclass
class RetriverConfig:
    data_dir: str = "./data"
    persist_path: str = "./vector_db"
    db_type: str = "faiss"
    top_k: int = 2
    provider: str = "ollama"

class Retriever:
    """
    This is a semantic search retrival function that retrieves relevant context from faiss vector DB.
    This doesn't generate answers, just retrives the suitable context/content.
    """
    def __init__(self, config: Optional[RetriverConfig] = None):
        self.config = config or RetriverConfig()
        self.embeddings = get_embeding_model(provider=self.config.provider)

        if VectorStoreManager.exists(self.config.persist_path):
            self.store = VectorStoreManager.load(embeddings=self.embeddings, persist_path=self.config.persist_path, dbtype=self.config.db_type)
            self.store_status = "loaded"
        else:
            self.store = runIngestion(dataDir=self.config.data_dir,
                                      persist_path=self.config.persist_path,
                                      dbtype=self.config.db_type,
                                      )
            self.store_status = "created"
    
    def retrieve(self, question: str, top_k: Optional[int] = None) -> list[Document]:
        if not question or not question.strip():
            raise ValueError("Question is empty")
        
        docs = self.store.similarity_search(query=question, fetch_k=top_k)
        return docs #self.store.similarity_search_with_score(query=question, k=self.config.top_k)
    
    def retrieve_with_score(self, question: str) -> list[tuple[Document, float]]:

        if not question or not question.strip():
            raise ValueError(f"The question {question} is empty.")
        
        return self.store.similarity_search_with_score(query=question, k=self.config.top_k)
    
    def health(self) -> dict[str, Any]:

        return {
            "vector_db_exists" : VectorStoreManager.exists(self.config.persist_path),
            "persist_path": self.config.persist_path,
            "dbtype": self.config.db_type,
            "top_k": self.config.top_k,
            "store_status": getattr(self, "store_status","unknown")
        }

    # def _pretty_print_docs(docs: list[Document]) -> None:
    #     for i, d in enumerate(docs, start=1):
    #         text = (d.page_content or "").strip().replace("\n", "")
    #         print(f"\n--- Result {i} ---")
    #         print(text[:400] + ("..." if len(text) > 400 else ""))


    def format_context(self, docs: List[Document], max_chars: int = 10_000) -> str:
        """
        Creates a context string from Documents.
        Includes small metadata line to help trace sources.
        """
        parts: list[str] = []
        used = 0

        for i, d in enumerate(docs):
            text = (d.page_content or "").strip()
            if not text:
                continue

            meta = d.metadata or {}
            source = meta.get("source") or meta.get("file_path") or meta.get("filename") or "unknown"
            header = f"[Chunk {i+1} | source={source}]"

            block = f"{header}\n{text}\n"
            if used + len(block) > max_chars:
                remaining = max_chars - used
                if remaining > 0:
                    parts.append(block[:remaining])
                parts.append("\n[Context truncated]\n")
                break

            parts.append(block)
            used += len(block)

        return "\n---\n".join(parts).strip()



# if __name__ == "__main__":
#     r = Retriever()
#     docs = r.retrieve("What does RAG stand for?", top_k=3)
#     print("Docs returned:", len(docs))
#     print("Top preview:", docs[0].page_content[:120])
#     ctx = r.format_context(docs)
#     print("Context chars:", len(ctx))  