import logging
from pathlib import Path

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.db.vector_store import VectorStoreManager
from app.utils.file_loader import load_documents


logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self) -> None:
        self.vector_store_manager = VectorStoreManager()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def ingest_file(self, file_path: Path) -> dict[str, int]:
        documents = load_documents(file_path)
        cleaned_documents = [self._clean_document(document) for document in documents]
        chunked_documents = self._split_documents(cleaned_documents)

        logger.info("Prepared %s chunks from %s", len(chunked_documents), file_path.name)
        self.vector_store_manager.add_documents(chunked_documents)

        return {"chunks_indexed": len(chunked_documents)}

    def _split_documents(self, documents: list[Document]) -> list[Document]:
        split_documents = self.text_splitter.split_documents(documents)

        for index, document in enumerate(split_documents):
            document.metadata["chunk_id"] = index
            document.metadata["source"] = document.metadata.get("source", "unknown")

        return split_documents

    @staticmethod
    def _clean_document(document: Document) -> Document:
        cleaned_text = " ".join(document.page_content.replace("\x00", " ").split())
        metadata = dict(document.metadata)
        return Document(page_content=cleaned_text, metadata=metadata)
