##########################################
# 
##########################################
from llm import getllm
import requests
from langchain_core.embeddings import Embeddings


class OllamaEmbeddings(Embeddings): 
    def __init__(self, provider: str = "ollama"):
        base = getllm(provide=provider).rstrip("/")
        self.url = base if base.endswith("/api/embeddings") else f"{base}/api/embeddings"
        self.modelName = "nomic-embed-text"
    
    def _embade_one(self, text:str) -> list[float]:
        payload = {"model": self.modelName, "prompt":text}
        response = requests.post(url=self.url, json=payload, timeout=60)
        response.raise_for_status
        if response.status_code == 200:
            return response.json()["Embeddings"]
    
    def embed_query(self, text: str) -> list[float]:
        return self._embade_one(text=text)

    def embade_documents(self, texts:list[str]) -> list[list[float]]:
        return [self._embade_one(t) for t in texts]



def get_embading_model(provider: str = "ollama") -> Embeddings:
    return OllamaEmbeddings(provider=provider)

# def get_embedding_model(provider: str, text: str) -> list[float]:
#     model = getllm(provide=provider)
#     #print(model)
    
#     payload = {
#         "model": "nomic-embed-text",
#         "prompt" : text
#     }
#     #print(payload)

#     response = requests.post(url=model, json=payload)
#     if response.status_code == 200:
#         #print("Embedding obtained successfully.")
#         return response.json()["embedding"]
#     else:
#         raise ValueError(f"Error getting embedding: {response.status_code} - {response.text}")  

# #res = get_embedding_model(provider="ollama", text="RAG uses embeddings for semantic search")
# #print(res)

# OllamaEmbeddings()