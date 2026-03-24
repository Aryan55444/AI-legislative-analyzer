from typing import Literal

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str
    chunk_id: int
    excerpt: str


class UploadResponse(BaseModel):
    message: str
    document_name: str
    stored_path: str
    chunks_indexed: int


class AnalyzeRequest(BaseModel):
    query: str
    role: Literal["citizen", "lawyer", "business", "regulator"] = "citizen"
    detail_level: Literal["short", "medium", "detailed"] = "medium"
    top_k: int = Field(default=4, ge=1, le=10)


class AnalysisResponse(BaseModel):
    summary: str
    key_points: list[str]
    risks: list[str]
    affected_groups: list[str]
    simplified_explanation: str
    citations: list[Citation] = Field(default_factory=list)
