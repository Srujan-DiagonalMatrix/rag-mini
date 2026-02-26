
class AppConfig():
    def __init__(self,
                ollama_base_url: str,
                openai_api_key: str,
                openai_model: str,
                chunk_size: int,
                chunk_overlap: int,
                top_k: int,
                temperature: float,
                max_tokens: int,
                data_dir: str = "./data",
                persist_path: str = "./vector_db",
                dbtype: str = "faiss",
                ollama_embedded_model: str = "nomic-embed-text"):
        pass

    def load_config() -> AppConfig:
        """loads .env + defaults"""
        pass

    def validate_config(cfg: AppConfig) -> None:
        """raises clear errors if missing required config"""
        pass