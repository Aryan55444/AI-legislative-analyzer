import logging

from fastapi import FastAPI

from app.config import settings
from app.routes.analyze import router as analyze_router
from app.routes.upload import router as upload_router


logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="AI Legislative Analyzer",
    description="API for uploading legal documents and generating grounded analysis.",
    version="1.0.0",
)

app.include_router(upload_router)
app.include_router(analyze_router)
