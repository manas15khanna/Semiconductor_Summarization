from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Job, Project, TimelineEvent
from app.settings import OLLAMA_MODEL
from app.services.project_service import ProjectService


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
templates.env.globals["ollama_model"] = OLLAMA_MODEL
project_service = ProjectService()


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    dashboard = project_service.get_system_dashboard(db)
    return templates.TemplateResponse("index.html", {"request": request, "dashboard": dashboard, "page_name": "Dashboard"})


@router.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request, db: Session = Depends(get_db)):
    overview = project_service.get_projects_overview(db)
    return templates.TemplateResponse("projects.html", {"request": request, "overview": overview, "page_name": "Projects"})


@router.get("/projects/{project_id}", response_class=HTMLResponse)
def project_dashboard(project_id: int, request: Request, db: Session = Depends(get_db)):
    dashboard = project_service.get_project_dashboard(db, project_id)
    timeline = project_service.get_project_timeline(db, project_id)
    project = db.query(Project).filter(Project.id == project_id).first()
    documents = project.documents if project else []
    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "dashboard": dashboard,
            "timeline": timeline,
            "documents": documents,
            "page_name": "Project Dashboard",
        },
    )


@router.get("/projects/{project_id}/upload", response_class=HTMLResponse)
def upload_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    jobs = db.query(Job).filter(Job.project_id == project_id).order_by(Job.created_at.desc()).limit(12).all()
    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "project": project, "jobs": jobs, "page_name": "Upload Documents"},
    )


@router.get("/documents/{document_id}", response_class=HTMLResponse)
def document_view(document_id: int, request: Request, db: Session = Depends(get_db)):
    document = project_service.get_document_details(db, document_id)
    latest_summary = None
    if document.summaries:
        latest_summary = sorted(document.summaries, key=lambda item: item.created_at, reverse=True)[0]
    timeline = (
        db.query(TimelineEvent)
        .filter(TimelineEvent.project_id == document.project_id, TimelineEvent.source_document == document.filename)
        .order_by(TimelineEvent.event_date.asc(), TimelineEvent.id.asc())
        .all()
    )
    return templates.TemplateResponse(
        "document.html",
        {
            "request": request,
            "document": document,
            "timeline": timeline,
            "latest_summary": latest_summary,
            "page_name": "Document Viewer",
        },
    )


@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "results": [], "query": "", "filter_type": "all", "page_name": "Search"},
    )


@router.get("/projects/{project_id}/timeline", response_class=HTMLResponse)
def timeline_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    timeline = project_service.get_project_timeline(db, project_id)
    return templates.TemplateResponse(
        "timeline.html",
        {"request": request, "project": project, "timeline": timeline, "page_name": "Timeline"},
    )

from app.models import Decision, Risk, ActionItem

@router.get("/decisions", response_class=HTMLResponse)
def decisions_page(request: Request, db: Session = Depends(get_db)):
    decisions = db.query(Decision).order_by(Decision.id.desc()).all()
    return templates.TemplateResponse(
        "decisions.html",
        {"request": request, "decisions": decisions, "page_name": "Decisions"},
    )

@router.get("/risks", response_class=HTMLResponse)
def risks_page(request: Request, db: Session = Depends(get_db)):
    risks = db.query(Risk).order_by(Risk.id.desc()).all()
    return templates.TemplateResponse(
        "risks.html",
        {"request": request, "risks": risks, "page_name": "Risks"},
    )

@router.get("/actions", response_class=HTMLResponse)
def actions_page(request: Request, db: Session = Depends(get_db)):
    actions = db.query(ActionItem).order_by(ActionItem.id.desc()).all()
    return templates.TemplateResponse(
        "actions.html",
        {"request": request, "actions": actions, "page_name": "Actions"},
    )
