from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Any

class AskRequest(BaseModel):

    question: str
    top_k: Optional[int] = None


class AskResponse(BaseModel):
    
    question: str
    answer: str
    sources: list[dict[str, Any]]
    top_k: int

class IngestResponse(BaseModel):
    status: str
    persist_path: str
    db_type: str
    store_type: str

class HealthResponse(BaseModel):
    vector_db_exists: bool
    openai_ready: bool