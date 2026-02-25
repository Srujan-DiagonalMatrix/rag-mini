from embeddings import get_embading_model
from langchain_community.vectorstores import VectorStore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class VectorStoreManager():

    @staticmethod
    def buildFromDocuments(docs, embeddings, dbType="faiss") -> VectorStore:
        dbType = dbType.lower()

        if dbType == "faiss":
            return FAISS.from_documents(docs, embeddings)
        raise ValueError(f"Unsupported database type: {dbType}. Supported types: 'faiss'.")
    
    def save(store, persist_path):
        None
    
    def load(embeddings, persist_path, db_type="faiss") -> VectorStore:
        None
    
    def exists(persist_path) -> bool:
        None

docs = [
    Document(page_content="RAG uses embeddings for semantic search"),
    Document(page_content="FAISS stores vectors locally.")
    ]

embeddings = get_embading_model(provider="ollama")
print(embeddings)


# res = VectorStoreManager.buildFromDocuments(docs=docs, embeddings=get_embedding_model(provider="ollama", text="RAG uses embeddings for semantic search"), dbType="faiss")
# print(res)