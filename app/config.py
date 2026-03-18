import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    gemini_embedding_model: str = os.getenv(
        "GEMINI_EMBEDDING_MODEL",
        "models/gemini-embedding-001",
    )
    google_transport: str = os.getenv("GOOGLE_TRANSPORT", "rest")
    vector_store_dir: Path = Path(os.getenv("VECTOR_STORE_DIR", "storage/vector_store"))
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "storage/uploads"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
