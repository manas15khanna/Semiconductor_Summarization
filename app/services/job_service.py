import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Job


class JobService:
    def create_job(self, db: Session, project_id: int, document_id: int | None, filename: str, status: str = "processing") -> Job:
        job = Job(
            id=str(uuid.uuid4()),
            project_id=project_id,
            document_id=document_id,
            filename=filename,
            status=status,
            stage="Upload Complete",
            progress=10,
            updated_at=datetime.utcnow(),
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def update_job(self, db: Session, job_id: str, *, status: str | None = None, stage: str | None = None, progress: int | None = None, error_message: str | None = None) -> Job | None:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        if status is not None:
            job.status = status
        if stage is not None:
            job.stage = stage
        if progress is not None:
            job.progress = progress
        if error_message is not None:
            job.error_message = error_message
        job.updated_at = datetime.utcnow()
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def get_job(self, db: Session, job_id: str) -> Job | None:
        return db.query(Job).filter(Job.id == job_id).first()
