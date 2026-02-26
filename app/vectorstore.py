##############################################
# This function stores the vectors into Vector DB and retries.
##############################################
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
import os
from typing import List, Optional
from embeddings import get_embeding_model

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
     
#      docs = [
#           Document(page_content="RAG uses embeddings for semantic search."),
#           Document(page_content="I am getting confidence in programming"),
#           Document(page_content="I can connect the dots well.")
#      ]

#      embeddings = get_embeding_model("ollama")

#      store = VectorStoreManager.buildFromDocuments(docs, embeddings, dbtype="faiss")
#      print("Vector store built!")

#      results = store.similarity_search(query="What is RAG?", k=2)
#      print("\nTop Matches(in-memory)")
#      for r in results:
#           print(r.page_content)

#      persist_path = "./vector_db"
#      VectorStoreManager.save(store=store, persist_path=persist_path)
#      print(f"Saved at the persist_path {persist_path}")

#      loaded_store = VectorStoreManager.load(embeddings, persist_path, "faiss")
#      print("loaded store")

#      results2 = store.similarity_search(query="Where are vectors stored?", k=2)
#      for r in results2:
#           print(r.page_content)


