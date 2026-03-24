from app.config import settings

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError as exc:
    raise RuntimeError("langchain-google-genai must be installed to use Gemini embeddings.") from exc


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    return GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embedding_model,
        google_api_key=settings.google_api_key,
        transport=settings.google_transport,
    )
