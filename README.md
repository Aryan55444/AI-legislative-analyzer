# AI Legislative Analyzer

FastAPI service for uploading legal and policy documents, indexing them with Gemini embeddings, and answering questions with cited, retrieval-based analysis.

## What it does

- Accepts `PDF`, `TXT`, and `DOCX` files
- Splits documents into chunks for retrieval
- Stores embeddings in a local FAISS index
- Retrieves relevant chunks for a question
- Returns structured analysis with citations

## Project layout

```text
app/
  main.py
  config.py
  routes/
    upload.py
    analyze.py
  services/
    embedding.py
    ingestion.py
    rag_pipeline.py
    retriever.py
  models/
    schemas.py
  utils/
    file_loader.py
  db/
    vector_store.py
sample_data/
  sample_bill.txt
```

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your `GOOGLE_API_KEY` to `.env`, then start the app:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Open `http://127.0.0.1:8001/docs`.

## API flow

1. `POST /upload` saves the file and indexes its chunks.
2. `POST /analyze` retrieves relevant chunks and asks Gemini for a structured answer.
3. The app attaches citations from the retrieved chunks before returning the response.

## Example requests

Upload a document:

```bash
curl -X POST "http://127.0.0.1:8001/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_data/sample_bill.txt"
```

Analyze it:

```bash
curl -X POST "http://127.0.0.1:8001/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"Explain this law in simple terms\",\"role\":\"citizen\",\"detail_level\":\"short\",\"top_k\":4}"
```

## Notes

- FAISS is stored locally under `storage/vector_store`.
- Uploaded files are saved under `storage/uploads`.
- Use `LOG_LEVEL=DEBUG` in `.env` if you want more logs while developing.
