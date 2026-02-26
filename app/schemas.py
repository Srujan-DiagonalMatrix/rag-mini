from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    top_k: int | None

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItems]
    request_Id: str
    timings_ms: dict

class HealthResponse(BaseModel):
    status: str
    check: dict

class SoutrceItem(BaseModel):
    source: str
    chunk_id: str | int | None
    text_preview: str | None

