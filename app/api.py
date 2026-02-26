#################################################
# Endpoints:
# GET /health -> HealthResponse
# POST /ingest -> status payload
# POST /ask -> AskResponse

# uvicorn app.api:create_app --factory --reload --port 8001
##################################################
from fastapi import FastAPI

def create_app() -> FastAPI:
    """initializes RAGPipeline(config) & sets up routes"""
    pass

