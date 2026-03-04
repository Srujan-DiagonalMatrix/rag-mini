#################################################
# Endpoints:
# GET /health -> HealthResponse
# POST /ingest -> status payload
# POST /ask -> AskResponse

# uvicorn app.api:create_app --factory --reload --port 8001
##################################################
from fastapi import FastAPI
from app.rag_pipeline import AppConfig, RagPipeline
from app.schemas import AskRequest, AskResponse, IngestResponse, HealthResponse

app = FastAPI(title="Mini RAG Application", version="1.0.0")
pipe = RagPipeline(AppConfig())

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    result = pipe.ask(req.question, top_k=req.top_k)
    return result

@app.post("/health", response_model=HealthResponse)
def health():
    return pipe.health()

@app.post("/Ingest", response_model=IngestResponse)
def ingest():
    return pipe.health()