# AI Legislative Analyzer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![License](https://img.shields.io/badge/license-MIT-blue)

A modern API for uploading and analyzing **legal and policy documents**. Powered by Gemini embeddings, FAISS similarity search, and retrieval-augmented generation (RAG).

---

## Features

- Upload and index `PDF`, `TXT`, and `DOCX` files
- Fast chunking and embedding using Google Gemini and Langchain
- Blazing-fast local semantic search with FAISS
- Ask questions against your uploaded corpus and get retrieval-grounded answers with document citations
- All data stays local: No cloud storage required
- RESTful API with OpenAPI docs

---

## Architecture Overview

```
User ─► /upload ─► Ingestion (chunk/split ➜ embed ➜ FAISS index)
User ─► /analyze ─► Retrieve relevant chunks (FAISS) ─► Gemini LLM (answer generation) ─► Response with citations
FILES: Saved in storage/uploads | Embeddings: storage/vector_store
```

### Key Components
- **FastAPI** (API)
- **Gemini/Google AI** (Embedding & LLM, via `langchain-google-genai`)
- **Langchain** (Pipeline orchestration)
- **FAISS** (Vector DB, local disk)
- **pypdf, docx2txt** (Document parsing)

---

## Requirements
- Python 3.10+
- Google API Key for Gemini (free for most users: https://makersuite.google.com/app/apikey)

---

## Installation

1. **Clone this repo:**
   ```bash
   git clone https://github.com/Aryan55444/AI-legislative-analyzer
   cd AI-legislative-analyzer
   ```
2. **Create and activate a virtualenv:**
   - Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows:
     ```sh
     python -m venv .venv
     .venv\Scripts\activate
     ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API keys:**
     - Copy `.env.example` to `.env` and edit `GOOGLE_API_KEY`.

---

## Running Locally
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```
Open [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) for the interactive API documentation.

---

## API Reference

### POST `/upload`
Uploads and indexes a legal document.
- Accepts: `PDF`, `TXT`, `DOCX`
- Returns: Number of chunks indexed, document path.

**Example (curl):**
```bash
curl -X POST "http://127.0.0.1:8001/upload" \
  -F "file=@sample_data/sample_bill.txt"
```

### POST `/analyze`
Retrieves relevant chunks and returns a structured, cited answer via Gemini.

**Sample Body:**
```json
{
  "query": "Summarize this bill for a student",
  "role": "citizen",
  "detail_level": "short",
  "top_k": 4
}
```

**Example (curl):**
```bash
curl -X POST "http://127.0.0.1:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain this law in simple terms","role":"citizen","detail_level":"short","top_k":4}'
```

---

## Configuration & Environment Variables
| Key                 | Purpose                            | Example                 |
|---------------------|------------------------------------|-------------------------|
| `GOOGLE_API_KEY`    | Google LLM/embedding API key       | `sk-...`                |
| `GEMINI_MODEL`      | Gemini model for RAG (default: 2.5)| `gemini-2.5-flash`      |
| `VECTOR_STORE_DIR`  | FAISS index storage path           | `storage/vector_store`  |
| `UPLOAD_DIR`        | Uploaded files storage             | `storage/uploads`       |
| `LOG_LEVEL`         | Logging verbosity                  | `INFO` / `DEBUG`        |

---

## Project Structure
```
app/
  main.py           # FastAPI entrypoint
  routes/           # /upload and /analyze endpoints
  services/         # Embedding, ingestion, RAG logic
  utils/            # File/data loading utilities
  db/               # FAISS vector store wrapper
  models/           # Pydantic API schemas
storage/
  uploads/          # User-uploaded files
  vector_store/     # FAISS embeddings index
sample_data/        # Sample docs
```

---

## Contributing
PRs and suggestions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (or create one).

1. Fork & clone repo
2. Make changes on a new branch
3. Ensure lint & test pass
4. Open a pull request

---

## License
[MIT License](LICENSE)

---

## FAQ
- **Is my data private?** Yes, all files and embeddings remain local.
- **Which models are used?** By default, Gemini 2.5 (configurable).
- **Is GPU required?** No, FAISS runs on CPU.
- **Can I deploy to cloud?** Yes, just set env variables appropriately and deploy as a container or on your preferred cloud host.
- **Where do logs go?** Standard output, level set by `LOG_LEVEL`.

---

## Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/)
- [Langchain](https://python.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)
