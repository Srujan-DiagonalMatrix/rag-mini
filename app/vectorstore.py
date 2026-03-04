##############################################
# This function stores the vectors into Vector DB and retries.
##############################################
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
import os
from typing import List, Optional
from app.embeddings import get_embeding_model

class VectorStoreManager:
    """
    This provides an ability to interact with Vectior DB.
    """

    @staticmethod
    def buildFromDocuments(docs: list[Document],
                           embeddings: Embeddings,
                           dbtype: str = "faiss"):
            """
            This connects you with Vector DB.
            """
            dbtype = dbtype.lower()

            if dbtype == "faiss":
                 return FAISS.from_documents(docs, embeddings)
            
            raise ValueError(f"Unsupported database {dbtype}.")

    @staticmethod
    def save(store, persist_path: str) -> None:
        """
        This stores the embeddings in local path.
        """
        os.makedirs(persist_path, exist_ok=True)
        store.save_local(persist_path)
    
    @staticmethod
    def load(embeddings: Embeddings,
             persist_path: str,
             dbtype: str = "faiss"):
        """
        This loads embeddings from local path to FAISS DB.
        """
        
        dbtype = dbtype.lower()
        if dbtype == "faiss":
             if not VectorStoreManager.exists(persist_path):
                  raise FileNotFoundError(f"The provided file not exists {persist_path}")
             
             return FAISS.load_local(persist_path,
                                     embeddings,
                                     allow_dangerous_deserialization=True)
        raise ValueError(f"Unsupported datatypes {dbtype}, provide correct DB Type.")
    
    @staticmethod
    def exists(persist_path: str) -> bool:
        """
        Checks the path presence in local instance.
        """
        
        if not os.path.isdir(persist_path):
             return False
        
        faiss_file = os.path.join(persist_path, "index.faiss")
        pkl_file = os.path.join(persist_path, "index.pkl")

        return os.path.exists(faiss_file) and os.path.exists(pkl_file)


# if __name__ == "__main__":

#     docs = [
#         Document(page_content="RAG uses embeddings for semantic search.", metadata={"source": "mem"}),
#         Document(page_content="FAISS stores vectors locally.", metadata={"source": "mem"}),
#     ]

#     embeddings = get_embeding_model("ollama")
#     store = VectorStoreManager.buildFromDocuments(docs, embeddings, "faiss")

#     print("Search result:", store.similarity_search("What stores vectors?", k=1)[0].page_content)

#     persist_path = "./vector_db_test"
#     VectorStoreManager.save(store, persist_path)
#     print("Saved:", VectorStoreManager.exists(persist_path))

#     store2 = VectorStoreManager.load(embeddings, persist_path, "faiss")
#     print("Loaded search:", store2.similarity_search("What is RAG?", k=1)[0].page_content)
