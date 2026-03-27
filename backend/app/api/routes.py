from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.schemas import AskRequest, AskResponse, DocumentUploadResponse, HealthResponse
from app.services.ingestion import ingest_pdf_document

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/api/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing file name.",
        )

    is_pdf_by_name = file.filename.lower().endswith(".pdf")
    is_pdf_by_content_type = file.content_type in {"application/pdf", "application/x-pdf"}
    if not (is_pdf_by_name or is_pdf_by_content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    max_upload_bytes = settings.max_upload_mb * 1024 * 1024
    if len(file_bytes) > max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File is too large. Max size is {settings.max_upload_mb}MB.",
        )

    try:
        return ingest_pdf_document(file_name=file.filename, file_bytes=file_bytes, db=db)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/api/chat/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    return AskResponse(
        answer=(
            "Ingestion pipeline is now wired. Retrieval and LLM answer generation "
            "will be implemented in the next commits."
        ),
        sources=[],
    )
