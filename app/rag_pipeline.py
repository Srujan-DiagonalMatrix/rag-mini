##############################################
# This becomes the single “brain” callable used by CLI + API.
##############################################
print("✅ rag_pipeline module loaded:", __name__)

from pydantic.dataclasses import dataclass
from typing import Optional
from langchain_core.documents import Document
from app.retrieval import Retriever, RetriverConfig
from app.generation import AnswerGenerator, GenerationConfig
from app.vectorstore import VectorStoreManager
from app.llm import check_openai_ready
from app.ingestion import runIngestion

@dataclass
class AppConfig:
    data_dir: str = "./data"
    persist_path: str = "./vector_db"
    db_type: str = "faiss"
    top_k: int = 3
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 500


class RagPipeline():

    def __init__(self, config: Optional[AppConfig] = None):
        """wires up Retriever + AnswerGenerator"""
        self.config = config or AppConfig()

        self.retriver = Retriever(RetriverConfig(persist_path=self.config.persist_path,
                                 db_type=self.config.db_type,
                                 top_k=self.config.top_k,
                                 provider="ollama"))
        
        self.generator = AnswerGenerator(GenerationConfig(model=self.config.openai_model,
                                         temperature=self.config.temperature,
                                         max_tokens=self.config.max_tokens))

    def ingest(self) -> dict[str, any]:
        """returns status: created/loaded, doc count, chunk count"""
        store = runIngestion(dataDir=self.config.data_dir, 
                             persist_path=self.config.persist_path,
                             dbtype=self.config.db_type)
        
        return{
            "status": "loaded" if VectorStoreManager.exists(self.config.persist_path) else "created",
            "persist_path":self.config.persist_path,
            "dbtype":self.config.db_type,
            "store_type": type(store).__name__
        }
    
    def health(self) -> dict[str, any]:
        """checks: vector DB exists, Ollama reachable (optional ping), OpenAI key present"""
        return{
            "vector_db_exists": VectorStoreManager.exists(self.config.persist_path),
            "openai_ready": check_openai_ready()
        }
    
    def _build_sources(self, docs: list[Document], preview_chars: int = 200) -> list[dict]:
        sources = []

        for i, d in enumerate(docs):
            meta = d.metadata or {}
            source = meta.get("source") or meta.get("file_path") or meta.get("filename") or "unknown"
            preview = (d.page_content or "").strip().replace("\n","")
            sources.append(
                {"rank": i + 1,
                 "source": source,
                 "preview": preview,
                 "metadata": meta}
            )
        
        return sources

    def ask(self, question: str, top_k: Optional[int] = None) -> dict[str, any]:
        """calls retrieve() → builds context → calls generate_with_sources()
        returns response dict (answer + sources + timings)"""
        q = (question or "").strip()
        if not q:
            raise ValueError("Question can't be empty.")
        
        docs = self.retriver.retrieve(question=q, top_k=top_k)
        context = self.retriver.format_context(docs=docs)

        answer = self.generator.generate_answer(question=q, context=context)

        return {
            "question":q,
            "answer":answer,
            "sources":self._build_sources(docs=docs),
            "top_k": top_k if top_k is not None else self.config.top_k           
        }
    
# if __name__ == "__main__":
#     print("✅ rag_pipeline running as __main__")
#     pipe = RagPipeline(AppConfig())
#     out = pipe.ask("What does RAG stand for?", top_k=3)
#     print(out["answer"])
#     print("Sources:", [s["source"] for s in out["sources"]])    