from pathlib import Path

from langchain.schema import Document
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader


def load_documents(file_path: Path) -> list[Document]:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        documents = PyPDFLoader(str(file_path)).load()
    elif suffix == ".docx":
        documents = Docx2txtLoader(str(file_path)).load()
    elif suffix == ".txt":
        documents = TextLoader(str(file_path), encoding="utf-8").load()
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    for document in documents:
        document.metadata["source"] = file_path.name

    return documents
