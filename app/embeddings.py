##########################################
# 
##########################################
from llm import getllm
import requests

def get_embedding_model(provider: str, text: str) -> list[float]:
    model = getllm(provide=provider)
    #print(model)
    
    payload = {
        "model": "nomic-embed-text",
        "prompt" : text
    }
    #print(payload)

    response = requests.post(url=model, json=payload)
    if response.status_code == 200:
        #print("Embedding obtained successfully.")
        return response.json()["embedding"]
    else:
        raise ValueError(f"Error getting embedding: {response.status_code} - {response.text}")  

#res = get_embedding_model(provider="ollama", text="RAG uses embeddings for semantic search")
#print(res)