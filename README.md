# Summarization and Decision Traceability System for Semiconductor Product Development Lifecycle

Local-first FastAPI application for ingesting engineering documents, generating summaries with Ollama, extracting decisions/action items/risks/timeline events, and searching the resulting knowledge base.

## Stack

- FastAPI
- SQLite
- SQLAlchemy
- Jinja2
- Vanilla JavaScript
- Ollama with `gemma3:1b`
- `pdfplumber` and `python-docx`

## Features

- Create projects
- Upload `TXT`, `MD`, `PDF`, and `DOCX` documents
- Store metadata and extracted raw text
- Skip unchanged files using content hashes
- Generate structured summaries
- Extract decisions, action items, risks, and timeline events
- Search across document content and generated knowledge
- Process uploads asynchronously with background jobs and polling
- View project dashboards, timelines, tabs, and recent activity
- Drag-and-drop or click-to-select multiple file uploads with progress
- Show risk traffic lights using dataset metadata and inferred severity
- Run fully offline against a local Ollama instance

## Project Structure

```text
app/
  config.py
  database/
  models/
  routes/
  services/
  static/
  templates/
  utils/
data/
  database/
  generated_summaries/
  projects/
  uploads/
main.py
requirements.txt
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment settings:

```bash
copy .env.sample .env
```

On PowerShell:

```powershell
Copy-Item .env.sample .env
```

4. Start Ollama:

```bash
ollama serve
```

5. Pull or run the model locally:

```bash
ollama run gemma3:1b
```

6. Start the application:

```bash
uvicorn main:app --reload
```

7. Open:

```text
http://127.0.0.1:8000
```

## Notes

- Database initialization runs automatically on startup.
- Lightweight migration logic adds missing columns for the current schema on startup.
- Generated summaries are also written to `data/generated_summaries/`.
- If Ollama is unavailable, document upload succeeds only until analysis is attempted; ensure `ollama serve` is running first.

## API Endpoints

- `GET /api/health`
- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `POST /api/projects/{project_id}/documents`
- `GET /api/documents/{document_id}`
- `POST /api/documents/{document_id}/summarize`
- `GET /api/projects/{project_id}/timeline`
- `GET /api/decisions`
- `GET /api/jobs/{job_id}`
- `GET /api/search?query=...`

## Phase 1 Scope

Included:

- Local project/document management
- Text extraction for supported file types
- Ollama-based summarization and structured extraction
- Project dashboard, document view, search, and timeline pages

Excluded:

- OCR
- Authentication
- User roles
- Vector databases
- Docker
- Cloud deployment
- Email notifications
- WebSockets
- Microservices
