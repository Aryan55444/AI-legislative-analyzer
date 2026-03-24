import logging

from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool

from app.models.schemas import AnalyzeRequest, AnalysisResponse
from app.services.rag_pipeline import RAGPipeline


logger = logging.getLogger(__name__)
router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(request: AnalyzeRequest) -> AnalysisResponse:
    pipeline = RAGPipeline()

    try:
        return await run_in_threadpool(pipeline.analyze, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Analysis request failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc
