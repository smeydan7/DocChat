from io import BytesIO
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas import DocumentUploadResponse


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Failed to read PDF file.") from exc

    page_texts: list[str] = []
    for page in reader.pages:
        extracted = page.extract_text() or ""
        if extracted.strip():
            page_texts.append(extracted)

    if not page_texts:
        raise ValueError("No extractable text found in this PDF.")

    return "\n\n".join(page_texts)


def _split_into_chunks(raw_text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = [chunk.strip() for chunk in splitter.split_text(raw_text) if chunk.strip()]
    if not chunks:
        raise ValueError("Unable to create chunks from the uploaded PDF.")
    return chunks


def ingest_pdf_document(*, file_name: str, file_bytes: bytes, db: Session) -> DocumentUploadResponse:
    raw_text = _extract_text_from_pdf(file_bytes)
    chunks = _split_into_chunks(raw_text)

    document_id = str(uuid4())

    try:
        db.execute(
            text(
                """
                INSERT INTO documents (id, file_name)
                VALUES (:id, :file_name)
                """
            ),
            {"id": document_id, "file_name": file_name},
        )

        for chunk_index, chunk_text in enumerate(chunks):
            db.execute(
                text(
                    """
                    INSERT INTO document_chunks (id, document_id, chunk_index, chunk_text, embedding)
                    VALUES (:id, :document_id, :chunk_index, :chunk_text, NULL)
                    """
                ),
                {
                    "id": str(uuid4()),
                    "document_id": document_id,
                    "chunk_index": chunk_index,
                    "chunk_text": chunk_text,
                },
            )

        db.commit()
    except Exception:  # noqa: BLE001
        db.rollback()
        raise

    return DocumentUploadResponse(
        document_id=document_id,
        file_name=file_name,
        chunk_count=len(chunks),
        message="Document uploaded, text extracted, and chunks stored.",
    )
