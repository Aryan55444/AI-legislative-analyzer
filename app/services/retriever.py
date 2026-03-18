import logging

from langchain.schema import Document

from app.db.vector_store import VectorStoreManager


logger = logging.getLogger(__name__)


class RetrieverService:
    def __init__(self) -> None:
        self.vector_store_manager = VectorStoreManager()

    def retrieve(self, query: str, top_k: int = 4) -> list[Document]:
        vector_store = self.vector_store_manager.load_vector_store()
        documents = vector_store.similarity_search(query, k=top_k)
        logger.info("Retrieved %s chunks for query", len(documents))
        return documents
