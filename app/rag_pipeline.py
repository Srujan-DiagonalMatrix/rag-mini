##############################################
# This becomes the single “brain” callable used by CLI + API.
##############################################

from ingestion import runIngestion

class RagPipeline():

    def __init__(self, config: AppConfig):
        """wires up Retriever + AnswerGenerator"""
        pass

    def ask(self, question: str) -> str:
        """calls retrieve() → builds context → calls generate_with_sources()
        returns response dict (answer + sources + timings)"""
        pass

    def health(self) -> dict:
        """checks: vector DB exists, Ollama reachable (optional ping), OpenAI key present"""
        pass

    def ingest(self) -> dict:
        """returns status: created/loaded, doc count, chunk count"""
        store = runIngestion()
    