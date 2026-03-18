import re

from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.models.schemas import AnalyzeRequest, AnalysisResponse, Citation
from app.services.retriever import RetrieverService


SYSTEM_PROMPT = """
You explain legal and policy documents in plain, natural language.
Use only the retrieved context. If the context is missing or incomplete, say so.
Match the audience role and detail level.
Return clean text that fits the response schema.
"""


class RAGPipeline:
    def __init__(self) -> None:
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is not configured.")

        self.retriever = RetrieverService()
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            transport=settings.google_transport,
        )
        self.structured_llm = self.llm.with_structured_output(AnalysisResponse)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT.strip()),
                (
                    "user",
                    """
                    Question: {query}
                    Audience: {role}
                    Detail level: {detail_level}

                    Context:
                    {context}

                    Write a grounded answer using only the context above.
                    Keep the tone natural and direct.
                    Do not use markdown, labels, or bold text.
                    Keep list items short and clear.
                    In affected_groups, return plain group names or short descriptions.
                    """.strip(),
                ),
            ]
        )

    def analyze(self, request: AnalyzeRequest) -> AnalysisResponse:
        documents = self.retriever.retrieve(request.query, request.top_k)
        if not documents:
            raise ValueError("No indexed documents found. Upload a document before analyzing.")

        context = self._build_context(documents)
        response = self.structured_llm.invoke(
            self.prompt.format_messages(
                query=request.query,
                role=request.role,
                detail_level=request.detail_level,
                context=context,
            )
        )
        analysis = self._humanize_response(AnalysisResponse.model_validate(response))
        analysis.citations = self._build_citations(documents)
        return analysis

    @staticmethod
    def _build_context(documents: list) -> str:
        sections: list[str] = []
        for document in documents:
            source = document.metadata.get("source", "unknown")
            chunk_id = document.metadata.get("chunk_id", "n/a")
            sections.append(f"[Source: {source} | Chunk: {chunk_id}]\n{document.page_content}")
        return "\n\n".join(sections)

    @staticmethod
    def _build_citations(documents: list) -> list[Citation]:
        citations: list[Citation] = []
        for document in documents:
            citations.append(
                Citation(
                    source=document.metadata.get("source", "unknown"),
                    chunk_id=int(document.metadata.get("chunk_id", 0)),
                    excerpt=document.page_content[:220].strip(),
                )
            )
        return citations

    @classmethod
    def _humanize_response(cls, analysis: AnalysisResponse) -> AnalysisResponse:
        analysis.summary = cls._clean_text(analysis.summary)
        analysis.key_points = [cls._clean_text(item) for item in analysis.key_points]
        analysis.risks = [cls._clean_text(item) for item in analysis.risks]
        analysis.affected_groups = [cls._clean_text(item) for item in analysis.affected_groups]
        analysis.simplified_explanation = cls._clean_text(analysis.simplified_explanation)
        return analysis

    @staticmethod
    def _clean_text(value: str) -> str:
        cleaned = re.sub(r"[*_`#>]+", "", value)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned.removeprefix(": ").strip()
