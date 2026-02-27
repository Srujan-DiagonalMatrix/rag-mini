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
    """
    This is a semantic search retrival function that retrieves relevant context from faiss vector DB.
    This doesn't generate answers, just retrives the suitable context/content.
    """
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
    
    def retrieve_with_score(self, question: str) -> list[tuple[Document, float]]:

        if not question or not question.strip():
            raise ValueError(f"The question {question} is empty.")
        
        return self.store.similarity_search_with_score(query=question, k=self.config.top_k)
    
    def health(self) -> dict[str, any]:

        return {
            "vector_db_exists" : VectorStoreManager.exists(self.config.persist_path),
            "persist_path": self.config.persist_path,
            "dbtype": self.config.db_type,
            "top_k": self.config.top_k,
            "store_status": getattr(self, "store_status","unknown")
        }

def _pretty_print_docs(docs: list[Document]) -> None:
    for i, d in enumerate(docs, start=1):
        text = (d.page_content or "").strip().replace("\n", "")
        print(f"\n--- Result {i} ---")
        print(text[:400] + ("..." if len(text) > 400 else ""))


if __name__ == "__main__":
    cfg = AppConfig(data_dir="./data",
                    persist_path="./vector_db",
                    db_type="faiss",
                    top_k=2)
    
    rag = RagPipeline(cfg)
    print("Health: ", rag.health())

    question = "What is this document is all about?"
    docs = rag.retrieve(question=question)
    for doc in docs:
        print("The doc is --> ", doc)
    
    score = rag.retrieve_with_score(question=question)
    for ques_score in score:
        print("the score is --> ", ques_score[1])

    



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