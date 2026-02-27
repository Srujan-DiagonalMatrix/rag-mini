from langchain_core.documents import Document

class Retriver():
    def __init__(self, persist_path: str, dbtype: str, provider: str, top_k: int):
        """stores config, loads embeddings model config"""
        pass

    def load_store(self) -> any:
        """loads FAISS store via VectorStoreManager.load(...)"""
        pass

    def retrieve(self, question: str) -> list[Document]:
        """embeds question internally (FAISS does it via embeddings) and returns top-k docs"""
        pass

    def retrieve_with_scores(self, question: str) -> list[tuple[Document, float]]:
        """if you want similarity scores for debugging/observability"""
        pass

    def format_context(self, docs: list[Document]) -> str:
        """turns docs into a single context string (also attaches metadata formatting)"""
        pass