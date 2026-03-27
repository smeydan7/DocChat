from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class DocumentUploadResponse(BaseModel):
    document_id: str
    file_name: str
    chunk_count: int
    message: str


class AskRequest(BaseModel):
    question: str


class SourceChunk(BaseModel):
    document_id: str
    chunk_index: int
    text: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
