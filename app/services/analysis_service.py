from pathlib import Path

from sqlalchemy.orm import Session

from app.config import SUMMARIES_DIR
from app.models import ActionItem, Decision, Document, Risk, Summary, TimelineEvent
from app.services.document_service import extract_text
from app.services.job_service import JobService
from app.services.ollama_service import OllamaService
from app.utils.file_utils import ensure_text


class AnalysisService:
    def __init__(self, ollama_service: OllamaService | None = None):
        self.ollama = ollama_service or OllamaService()
        self.job_service = JobService()

    def process_document(self, db: Session, document: Document, job_id: str | None = None) -> None:
        raw_text = ensure_text(document.raw_text)
        if not raw_text:
            return

        self._clear_prior_analysis(db, document)

        self._update_stage(db, job_id, "Generating Summary", 40)
        summary_text = self.ollama.generate_summary(raw_text)
        summary = Summary(
            project_id=document.project_id,
            document_id=document.id,
            summary_type="document",
            summary_text=summary_text,
        )
        db.add(summary)
        self._write_summary_file(document, summary_text)
        db.commit()

        self._update_stage(db, job_id, "Extracting Decisions", 55)
        for item in self.ollama.extract_decisions(raw_text):
            db.add(
                Decision(
                    project_id=document.project_id,
                    document_id=document.id,
                    title=ensure_text(item.get("title")),
                    description=ensure_text(item.get("description")),
                    owner=ensure_text(item.get("owner")),
                    status=ensure_text(item.get("status")),
                    decision_date=ensure_text(item.get("decision_date")),
                )
            )
        db.commit()

        self._update_stage(db, job_id, "Extracting Actions", 70)
        for item in self.ollama.extract_actions(raw_text):
            db.add(
                ActionItem(
                    project_id=document.project_id,
                    document_id=document.id,
                    description=ensure_text(item.get("description")),
                    owner=ensure_text(item.get("owner")),
                    due_date=ensure_text(item.get("due_date")),
                    status=ensure_text(item.get("status")),
                )
            )
        db.commit()

        self._update_stage(db, job_id, "Extracting Risks", 85)
        for item in self.ollama.extract_risks(raw_text):
            db.add(
                Risk(
                    project_id=document.project_id,
                    document_id=document.id,
                    description=ensure_text(item.get("description")),
                    impact=ensure_text(item.get("impact")),
                    mitigation=ensure_text(item.get("mitigation")),
                    owner=ensure_text(item.get("owner")),
                )
            )
        db.commit()

        self._update_stage(db, job_id, "Updating Timeline", 95)
        for item in self.ollama.extract_timeline(raw_text):
            db.add(
                TimelineEvent(
                    project_id=document.project_id,
                    source_document=document.filename,
                    event_date=ensure_text(item.get("event_date")),
                    title=ensure_text(item.get("title")),
                    description=ensure_text(item.get("description")),
                )
            )

        db.commit()
        document.processing_status = "complete"
        db.add(document)
        db.commit()
        self._update_stage(db, job_id, "Complete", 100, status="complete")

    def process_document_from_storage(self, db: Session, document: Document, job_id: str | None = None) -> None:
        self._update_stage(db, job_id, "Extracting Text", 20)
        file_path = Path(document.storage_path)
        file_bytes = file_path.read_bytes()
        document.raw_text = extract_text(file_bytes, document.file_type)
        document.processing_status = "processing"
        db.add(document)
        db.commit()
        self.process_document(db, document, job_id=job_id)

    def _clear_prior_analysis(self, db: Session, document: Document) -> None:
        db.query(Summary).filter(Summary.document_id == document.id).delete()
        db.query(Decision).filter(Decision.document_id == document.id).delete()
        db.query(ActionItem).filter(ActionItem.document_id == document.id).delete()
        db.query(Risk).filter(Risk.document_id == document.id).delete()
        db.query(TimelineEvent).filter(
            TimelineEvent.project_id == document.project_id,
            TimelineEvent.source_document == document.filename,
        ).delete()
        db.commit()

    def _write_summary_file(self, document: Document, summary_text: str) -> None:
        path = Path(SUMMARIES_DIR) / f"document_{document.id}_summary.txt"
        path.write_text(summary_text, encoding="utf-8")

    def _update_stage(self, db: Session, job_id: str | None, stage: str, progress: int, status: str = "processing") -> None:
        if not job_id:
            return
        self.job_service.update_job(db, job_id, stage=stage, progress=progress, status=status)
