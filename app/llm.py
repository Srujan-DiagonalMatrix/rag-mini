###############################################
# This supplies the LLM details.
###############################################
from dotenv import load_dotenv
load_dotenv()

def getllm(provide: str) -> str:
    openAi = ""
    ollama = "http://localhost:11434/api/embeddings"

    if provide == "openAi":
        return openAi
    elif provide == "ollama":
        return ollama
    else:
        raise ValueError("Invalid provider specified. Choose 'openAi' or 'ollama'.")

