from pathlib import Path
import re

from fastapi import HTTPException, UploadFile
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.config import PROJECTS_DIR, UPLOADS_DIR
from app.database.session import SessionLocal
from app.models import ActionItem, Decision, Document, Job, Project, Risk, Summary, TimelineEvent
from app.services.analysis_service import AnalysisService
from app.services.job_service import JobService
from app.utils.dataset_utils import get_dataset_metadata, infer_risk_severity, severity_emoji
from app.utils.file_utils import detect_file_type, generate_content_hash, sanitize_filename, unique_output_path


class ProjectService:
    def __init__(self):
        self.job_service = JobService()

    def create_project(self, db: Session, name: str, description: str) -> Project:
        existing = db.query(Project).filter(func.lower(Project.name) == name.lower()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Project name already exists.")

        project = Project(name=name.strip(), description=description.strip())
        db.add(project)
        db.commit()
        db.refresh(project)

        (PROJECTS_DIR / str(project.id)).mkdir(parents=True, exist_ok=True)
        return project

    def upload_document(self, db: Session, project_id: int, upload: UploadFile) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")

        file_bytes = upload.file.read()
        file_type = detect_file_type(upload.filename or "")
        content_hash = generate_content_hash(file_bytes)

        existing = (
            db.query(Document)
            .filter(Document.project_id == project_id, Document.content_hash == content_hash)
            .first()
        )
        if existing:
            return {"document": existing, "skipped": True}

        filename = sanitize_filename(upload.filename or "document")
        project_upload_dir = UPLOADS_DIR / str(project_id)
        project_upload_dir.mkdir(parents=True, exist_ok=True)
        output_path = unique_output_path(project_upload_dir, filename)
        output_path.write_bytes(file_bytes)

        document = Document(
            project_id=project_id,
            filename=output_path.name,
            file_type=file_type,
            content_hash=content_hash,
            raw_text="",
            storage_path=str(output_path),
            processing_status="queued",
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        job = self.job_service.create_job(db, project_id, document.id, document.filename)
        return {"document": document, "job": job, "skipped": False}

    def process_document_job(self, document_id: int, job_id: str) -> None:
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                self.job_service.update_job(db, job_id, status="failed", stage="Failed", progress=100, error_message="Document not found.")
                return
            if document.storage_path:
                AnalysisService().process_document_from_storage(db, document, job_id=job_id)
            else:
                document.processing_status = "processing"
                db.add(document)
                db.commit()
                AnalysisService().process_document(db, document, job_id=job_id)
        except Exception as exc:
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                document.processing_status = "failed"
                db.add(document)
                db.commit()
            self.job_service.update_job(db, job_id, status="failed", stage="Failed", progress=100, error_message=str(exc))
        finally:
            db.close()

    def get_project_dashboard(self, db: Session, project_id: int) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")

        total_documents = db.query(func.count(Document.id)).filter(Document.project_id == project_id).scalar() or 0
        total_decisions = db.query(func.count(Decision.id)).filter(Decision.project_id == project_id).scalar() or 0
        total_risks = db.query(func.count(Risk.id)).filter(Risk.project_id == project_id).scalar() or 0
        open_actions = (
            db.query(func.count(ActionItem.id))
            .filter(
                ActionItem.project_id == project_id,
                or_(ActionItem.status.is_(None), ActionItem.status == "", func.lower(ActionItem.status) != "closed"),
            )
            .scalar()
            or 0
        )
        closed_actions = (
            db.query(func.count(ActionItem.id))
            .filter(ActionItem.project_id == project_id, func.lower(ActionItem.status) == "closed")
            .scalar()
            or 0
        )
        recent_summary = (
            db.query(Summary)
            .filter(Summary.project_id == project_id)
            .order_by(Summary.created_at.desc())
            .first()
        )
        recent_uploads = (
            db.query(Document)
            .filter(Document.project_id == project_id)
            .order_by(Document.upload_date.desc())
            .limit(6)
            .all()
        )
        recent_activity = (
            db.query(TimelineEvent)
            .filter(TimelineEvent.project_id == project_id)
            .order_by(TimelineEvent.event_date.desc(), TimelineEvent.id.desc())
            .limit(8)
            .all()
        )
        recent_jobs = (
            db.query(Job)
            .filter(Job.project_id == project_id)
            .order_by(Job.created_at.desc())
            .limit(8)
            .all()
        )
        risk_register = []
        for item in get_dataset_metadata()["risks"]:
            risk_register.append(
                {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "owner": item.get("owner", ""),
                    "status": item.get("status", ""),
                    "severity": item.get("severity", ""),
                    "severity_emoji": severity_emoji(item.get("severity", "")),
                }
            )

        return {
            "project": project,
            "total_documents": total_documents,
            "total_decisions": total_decisions,
            "total_risks": total_risks,
            "open_actions": open_actions,
            "closed_actions": closed_actions,
            "recent_summary": recent_summary.summary_text if recent_summary else "",
            "recent_uploads": recent_uploads,
            "recent_activity": recent_activity,
            "recent_jobs": recent_jobs,
            "risk_register": risk_register,
        }

    def get_system_dashboard(self, db: Session) -> dict:
        projects = db.query(func.count(Project.id)).scalar() or 0
        documents = db.query(func.count(Document.id)).scalar() or 0
        decisions = db.query(func.count(Decision.id)).scalar() or 0
        risks = db.query(func.count(Risk.id)).scalar() or 0
        open_actions = (
            db.query(func.count(ActionItem.id))
            .filter(or_(ActionItem.status.is_(None), ActionItem.status == "", func.lower(ActionItem.status) != "closed"))
            .scalar()
            or 0
        )
        recent_uploads = db.query(Document).order_by(Document.upload_date.desc()).limit(8).all()
        recent_summary = db.query(Summary).order_by(Summary.created_at.desc()).first()
        recent_activity = db.query(TimelineEvent).order_by(TimelineEvent.event_date.desc(), TimelineEvent.id.desc()).limit(10).all()
        jobs = db.query(Job).order_by(Job.updated_at.desc()).limit(10).all()
        dataset = get_dataset_metadata()
        if not recent_activity:
            recent_activity = dataset["timeline"][-10:]
        return {
            "counts": {
                "projects": projects,
                "documents": documents,
                "decisions": decisions,
                "open_actions": open_actions,
                "risks": risks,
            },
            "recent_uploads": recent_uploads,
            "recent_activity": recent_activity,
            "recent_summary": recent_summary,
            "jobs": jobs,
            "dataset_summary": dataset["project_summary"],
            "risk_register": [
                {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "owner": item.get("owner", ""),
                    "status": item.get("status", ""),
                    "severity": item.get("severity", ""),
                    "severity_emoji": severity_emoji(item.get("severity", "")),
                }
                for item in dataset["risks"]
            ],
        }

    def get_document_details(self, db: Session, document_id: int) -> Document:
        document = (
            db.query(Document)
            .options(
                joinedload(Document.project),
                joinedload(Document.summaries),
                joinedload(Document.decisions),
                joinedload(Document.action_items),
                joinedload(Document.risks),
            )
            .filter(Document.id == document_id)
            .first()
        )
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")
        for risk in document.risks:
            severity = infer_risk_severity(risk.description, risk.impact)
            setattr(risk, "severity", severity)
            setattr(risk, "severity_emoji", severity_emoji(severity))
        return document

    def get_project_timeline(self, db: Session, project_id: int) -> list[TimelineEvent]:
        return (
            db.query(TimelineEvent)
            .filter(TimelineEvent.project_id == project_id)
            .order_by(TimelineEvent.event_date.asc(), TimelineEvent.id.asc())
            .all()
        )

    def search(self, db: Session, query: str, filter_type: str = "all") -> list[dict]:
        term = f"%{query.strip()}%"
        if not query.strip():
            return []

        project_map = {project.id: project.name for project in db.query(Project).all()}
        document_map = {doc.id: doc for doc in db.query(Document).all()}
        results: list[dict] = []

        normalized_filter = filter_type.lower()

        if normalized_filter in {"all", "documents"}:
            for document in db.query(Document).filter(Document.raw_text.ilike(term)).all():
                results.append(
                    self._result_item(
                        "Document",
                        project_map.get(document.project_id, ""),
                        document.filename,
                        document.raw_text,
                        query,
                        f"/documents/{document.id}",
                    )
                )

            for summary in db.query(Summary).filter(Summary.summary_text.ilike(term)).all():
                document = document_map.get(summary.document_id)
                results.append(
                    self._result_item(
                        "Summary",
                        project_map.get(summary.project_id, ""),
                        document.filename if document else "",
                        summary.summary_text,
                        query,
                        f"/documents/{summary.document_id}",
                    )
                )

        if normalized_filter in {"all", "decisions"}:
            for decision in db.query(Decision).filter(
                or_(Decision.title.ilike(term), Decision.description.ilike(term), Decision.owner.ilike(term))
            ).all():
                document = document_map.get(decision.document_id)
                snippet = " | ".join([decision.title, decision.description, decision.owner])
                results.append(
                    self._result_item(
                        "Decision",
                        project_map.get(decision.project_id, ""),
                        document.filename if document else "",
                        snippet,
                        query,
                        f"/documents/{decision.document_id}",
                    )
                )

        if normalized_filter in {"all", "actions"}:
            for action in db.query(ActionItem).filter(
                or_(ActionItem.description.ilike(term), ActionItem.owner.ilike(term), ActionItem.status.ilike(term))
            ).all():
                document = document_map.get(action.document_id)
                snippet = " | ".join([action.description, action.owner, action.status])
                results.append(
                    self._result_item(
                        "Action Item",
                        project_map.get(action.project_id, ""),
                        document.filename if document else "",
                        snippet,
                        query,
                        f"/documents/{action.document_id}",
                    )
                )

        if normalized_filter in {"all", "risks"}:
            for risk in db.query(Risk).filter(
                or_(Risk.description.ilike(term), Risk.impact.ilike(term), Risk.mitigation.ilike(term), Risk.owner.ilike(term))
            ).all():
                document = document_map.get(risk.document_id)
                snippet = " | ".join([risk.description, risk.impact, risk.mitigation, risk.owner])
                results.append(
                    self._result_item(
                        "Risk",
                        project_map.get(risk.project_id, ""),
                        document.filename if document else "",
                        snippet,
                        query,
                        f"/documents/{risk.document_id}",
                    )
                )

        return results

    def get_projects_overview(self, db: Session) -> dict:
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        dataset = get_dataset_metadata()
        return {
            "projects": projects,
            "dataset_summary": dataset["project_summary"],
            "reference_timeline": dataset["timeline"][:8],
        }

    def _result_item(self, result_type: str, project: str, document: str, source_text: str, query: str, link: str) -> dict:
        snippet = (source_text or "").replace("\n", " ").strip()
        snippet = self._highlight(snippet[:450], query)
        return {
            "result_type": result_type,
            "project": project,
            "document": document,
            "snippet": snippet,
            "link": link,
        }

    def _highlight(self, text: str, query: str) -> str:
        lower_text = text.lower()
        lower_query = query.lower().strip()
        if not lower_query or lower_query not in lower_text:
            return text
        start = max(lower_text.find(lower_query) - 60, 0)
        end = min(start + max(len(query) + 180, 220), len(text))
        snippet = text[start:end].strip()
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(lambda match: f"<mark>{match.group(0)}</mark>", snippet)
