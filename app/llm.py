###############################################
# This supplies the LLM details.
###############################################

from __future__ import annotations
import os
import requests
from dotenv import load_dotenv
load_dotenv()


def getllm(provide: str) -> str:

    if provide == "ollama":
        return os.getenv("OLLAMA_EMBEDDINGS").strip()
    else:
        raise ValueError("Invalid provider specified. Choose 'openAi' or 'ollama'.")

def get_ollama_embeddings_url() -> str:
    return getllm("ollama").rstrip("/")

def _get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY","").strip()
    return key

def _get_openai_base_url() -> str:
    base_url = os.getenv("OPENAI_BASE_URL").strip()
    return base_url

def call_openai_chat(messages: list[dict], model: str, temperature: float, max_tokens: int) -> str:

    api_key = _get_openai_key()
    if not api_key:
        raise ValueError("API Key is missing.")
    
    base_url = _get_openai_base_url()
    if not base_url:
        raise ValueError("Base is missing")
    
    deployment = "gpt-4o-mini"
    api_version = "2025-02-01-preview"

    url = f"{base_url}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

    # if base_url.endswith("/v1"):
    #     url = f"{base_url}/chat/completions"
    # else:
    #     url = f"{base_url}/v1/chat/completions"

    #url = base_url

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(url=url, json=payload, timeout=120, headers=headers)
    if not response.ok:
        raise RuntimeError(
            f"OpenAI request failed: {response.status_code}\n"
            f"URL: {url}\n"
            f"Body: {response.text[:1000]}"
        )

    response.raise_for_status()

    data = response.json()
    print(data)
    
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected openai format error: {data}") from e    

def check_openai_ready() -> bool:
    return bool(_get_openai_key())
