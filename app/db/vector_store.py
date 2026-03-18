import logging

from langchain_community.vectorstores import FAISS

from app.config import settings
from app.services.embedding import get_embedding_model


logger = logging.getLogger(__name__)


class VectorStoreManager:
    def __init__(self) -> None:
        self.embedding_model = get_embedding_model()
        self.store_path = settings.vector_store_dir
        self.store_path.mkdir(parents=True, exist_ok=True)

    def load_vector_store(self) -> FAISS:
        index_file = self.store_path / "index.faiss"
        if not index_file.exists():
            raise ValueError("Vector store is empty. Upload a document first.")

        logger.info("Loading vector store from %s", self.store_path)
        return FAISS.load_local(
            str(self.store_path),
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

    def add_documents(self, documents: list) -> None:
        index_file = self.store_path / "index.faiss"

        if index_file.exists():
            logger.info("Appending documents to existing vector store")
            vector_store = self.load_vector_store()
            vector_store.add_documents(documents)
        else:
            logger.info("Creating a new vector store")
            vector_store = FAISS.from_documents(documents, self.embedding_model)

        vector_store.save_local(str(self.store_path))
        logger.info("Vector store saved to %s", self.store_path)
