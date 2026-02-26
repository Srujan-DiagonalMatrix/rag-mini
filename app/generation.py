from langchain_core.documents import Document

class AnswerGenerator():
    def __init__(self, provider: str, model:str, temperature: float, max_token: int):
        pass

    def generate(self, question: str, contect: str) -> str:
        """uses prompt builder from prompts.py
        calls OpenAI chat client from llm.py"""
        pass

    def generate_with_sources(self, question: str, context: str, docs: list[Document]) -> dict:
        return {"answer":"",
                "sources":""}
    
    def post_process(self, answer: str) -> str:
        """trims, sanity checks, handles “I don’t know” style outputs"""
        pass