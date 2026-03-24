from fastapi import APIRouter, File, UploadFile

from app.schemas import AskRequest, AskResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    return {
        "message": "Upload endpoint scaffolded",
        "file_name": file.filename,
        "status": "not_implemented",
    }


@router.post("/api/chat/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    return AskResponse(
        answer=(
            "Groundwork complete. Retrieval and LLM answer generation "
            "will be implemented in the next commits."
        ),
        sources=[],
    )
