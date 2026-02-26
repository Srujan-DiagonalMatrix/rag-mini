##########################################
# This program generates embeddings, converts documents into embeddings.
##########################################
from llm import getllm
import requests
from langchain_core.embeddings import Embeddings


class OllamaEmbeddings(Embeddings): 
    """
    This returns the embeddings for the documents.
    """
    def __init__(self, provider: str = "ollama"):
        base = getllm(provide=provider).rstrip("/")
        self.url = base if base.endswith("/api/embeddings") else f"{base}/api/embeddings"
        self.modelName = "nomic-embed-text"
    
    def _embed_one(self, text:str) -> list[float]:
        payload = {"model": self.modelName, "prompt":text}
        response = requests.post(url=self.url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["embedding"]
    
    def embed_query(self, text: str) -> list[float]:
        return self._embed_one(text=text)

    def embed_documents(self, texts:list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in texts]


# This function creates the class object.
def get_embeding_model(provider: str = "ollama") -> Embeddings:
    return OllamaEmbeddings(provider=provider)
