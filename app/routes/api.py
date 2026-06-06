from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Decision, Document, Job, Project
from app.services.job_service import JobService
from app.services.project_service import ProjectService


router = APIRouter()
project_service = ProjectService()
job_service = JobService()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [{"id": project.id, "name": project.name, "description": project.description} for project in projects]


@router.post("/projects")
def create_project(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    project = project_service.create_project(db, name, description)
    return {"id": project.id, "name": project.name, "description": project.description}


@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    dashboard = project_service.get_project_dashboard(db, project_id)
    return {
        "project": {
            "id": dashboard["project"].id,
            "name": dashboard["project"].name,
            "description": dashboard["project"].description,
            "created_at": dashboard["project"].created_at.isoformat(),
        },
        "total_documents": dashboard["total_documents"],
        "total_decisions": dashboard["total_decisions"],
        "open_actions": dashboard["open_actions"],
        "closed_actions": dashboard["closed_actions"],
        "total_risks": dashboard["total_risks"],
        "recent_summary": dashboard["recent_summary"],
    }


@router.post("/projects/{project_id}/documents", status_code=202)
def upload_document(
    project_id: int,
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    items = []
    for upload in files:
        result = project_service.upload_document(db, project_id, upload)
        document = result["document"]
        if result["skipped"]:
            items.append(
                {
                    "id": document.id,
                    "filename": document.filename,
                    "file_type": document.file_type,
                    "skipped": True,
                    "job_id": None,
                }
            )
            continue
        job = result["job"]
        background_tasks.add_task(project_service.process_document_job, document.id, job.id)
        items.append(
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "skipped": False,
                "document_id": document.id,
                "job_id": job.id,
                "status": job.status,
                "stage": job.stage,
                "progress": job.progress,
            }
        )
    return {"items": items}


@router.get("/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = project_service.get_document_details(db, document_id)
    return {
        "id": document.id,
        "project_id": document.project_id,
        "filename": document.filename,
        "file_type": document.file_type,
        "upload_date": document.upload_date.isoformat(),
        "processing_status": document.processing_status,
        "raw_text": document.raw_text,
        "summaries": [{"type": item.summary_type, "text": item.summary_text} for item in document.summaries],
        "decisions": [
            {
                "title": item.title,
                "description": item.description,
                "owner": item.owner,
                "status": item.status,
                "decision_date": item.decision_date,
            }
            for item in document.decisions
        ],
        "actions": [
            {
                "description": item.description,
                "owner": item.owner,
                "due_date": item.due_date,
                "status": item.status,
            }
            for item in document.action_items
        ],
        "risks": [
            {
                "description": item.description,
                "impact": item.impact,
                "mitigation": item.mitigation,
                "owner": item.owner,
            }
            for item in document.risks
        ],
    }


@router.post("/documents/{document_id}/summarize")
def summarize_document(document_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    job = job_service.create_job(db, document.project_id, document.id, document.filename)
    background_tasks.add_task(project_service.process_document_job, document.id, job.id)
    return {"status": "queued", "document_id": document.id, "job_id": job.id}


@router.get("/projects/{project_id}/timeline")
def get_timeline(project_id: int, db: Session = Depends(get_db)):
    timeline = project_service.get_project_timeline(db, project_id)
    return [
        {
            "id": item.id,
            "event_date": item.event_date,
            "title": item.title,
            "description": item.description,
            "source_document": item.source_document,
        }
        for item in timeline
    ]


@router.get("/decisions")
def get_decisions(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Decision)
    if project_id:
        query = query.filter(Decision.project_id == project_id)
    results = query.order_by(Decision.id.desc()).all()
    return [
        {
            "id": item.id,
            "project_id": item.project_id,
            "document_id": item.document_id,
            "title": item.title,
            "description": item.description,
            "owner": item.owner,
            "status": item.status,
            "decision_date": item.decision_date,
        }
        for item in results
    ]


@router.get("/search")
def search(query: str, filter_type: str = "all", db: Session = Depends(get_db)):
    return {"results": project_service.search(db, query, filter_type=filter_type)}


@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return {
        "job_id": job.id,
        "status": job.status,
        "stage": job.stage,
        "progress": job.progress,
        "filename": job.filename,
        "document_id": job.document_id,
        "error_message": job.error_message,
    }
