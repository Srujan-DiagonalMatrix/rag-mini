from langchain_core.documents import Document
from dataclasses import dataclass
from embeddings import get_embeding_model
from vectorstore import VectorStoreManager
from ingestion import runIngestion

@dataclass
class AppConfig:
    data_dir: str = "./data"
    persist_path: str = "./vector_db"
    db_type: str = "faiss"
    top_k: int = 2

class RagPipeline:
    def __init__(self, config: AppConfig):
        self.config = config
        self.embeddings = get_embeding_model(provider="ollama")

        if VectorStoreManager.exists(self.config.persist_path):
            self.store = VectorStoreManager.load(embeddings=self.embeddings, persist_path=self.config.persist_path, dbtype=self.config.db_type)
            self.store_status = "loaded"
        else:
            self.store = runIngestion(dataDir=self.config.data_dir,
                                      persist_path=self.config.persist_path,
                                      dbtype=self.config.db_type,
                                      )
            self.store_status = "created"
    
    def retrieve(self, question: str) -> list[Document]:
        if not question or not question.strip():
            raise ValueError("Question is empty")
        
        return self.store.similarity_search_with_score(query=question, k=self.config.top_k)


# class AnswerGenerator():
#     def __init__(self, provider: str, model:str, temperature: float, max_token: int):
#         pass

#     def generate(self, question: str, contect: str) -> str:
#         """uses prompt builder from prompts.py
#         calls OpenAI chat client from llm.py"""
#         pass

#     def generate_with_sources(self, question: str, context: str, docs: list[Document]) -> dict:
#         return {"answer":"",
#                 "sources":""}
    
#     def post_process(self, answer: str) -> str:
#         """trims, sanity checks, handles “I don’t know” style outputs"""
#         pass