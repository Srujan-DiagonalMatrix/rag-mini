###############################################
# This supplies the LLM details.
###############################################
from dotenv import load_dotenv
load_dotenv()

def getllm(provide: str) -> str:
    openAi = "dummy-value"
    ollama = "http://localhost:11434/api/embeddings"

    if provide == "openAi":
        return openAi
    elif provide == "ollama":
        return ollama
    else:
        raise ValueError("Invalid provider specified. Choose 'openAi' or 'ollama'.")

def get_ollama_embeddings_url() -> str:
    pass

def get_openai_client() -> OpenAIClient:
    pass

def call_openai_chat(messages: list[dict], model: str, temperature: float, max_tokens: int) -> str:
    pass

def check_openai_ready() -> bool:
    pass