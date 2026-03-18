import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool

from app.config import settings
from app.models.schemas import UploadResponse
from app.services.ingestion import IngestionService


logger = logging.getLogger(__name__)
router = APIRouter(tags=["documents"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a name.")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".txt", ".docx"}:
        raise HTTPException(status_code=400, detail="Supported file types are PDF, TXT, and DOCX.")

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}_{Path(file.filename).name}"
    destination = settings.upload_dir / safe_name

    logger.info("Saving upload to %s", destination)
    content = await file.read()
    destination.write_bytes(content)

    service = IngestionService()

    try:
        result = await run_in_threadpool(service.ingest_file, destination)
    except Exception as exc:
        logger.exception("Document ingestion failed")
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {exc}") from exc

    return UploadResponse(
        message="Document uploaded and indexed successfully.",
        document_name=file.filename,
        stored_path=str(destination),
        chunks_indexed=result["chunks_indexed"],
    )
