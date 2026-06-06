from sqlalchemy import inspect, text

from app.database.base import Base
from app.database.session import engine
from app.models import action_item, decision, document, job, project, risk, summary, timeline_event


AUTO_MIGRATIONS = {
    "projects": {
        "description": "TEXT",
        "created_at": "DATETIME",
    },
    "documents": {
        "project_id": "INTEGER",
        "filename": "VARCHAR(255)",
        "file_type": "VARCHAR(50)",
        "upload_date": "DATETIME",
        "content_hash": "VARCHAR(64)",
        "storage_path": "VARCHAR(500)",
        "processing_status": "VARCHAR(50)",
        "raw_text": "TEXT",
    },
    "summaries": {
        "project_id": "INTEGER",
        "document_id": "INTEGER",
        "summary_type": "VARCHAR(50)",
        "summary_text": "TEXT",
        "created_at": "DATETIME",
    },
    "decisions": {
        "project_id": "INTEGER",
        "document_id": "INTEGER",
        "title": "VARCHAR(255)",
        "description": "TEXT",
        "owner": "VARCHAR(255)",
        "status": "VARCHAR(100)",
        "decision_date": "VARCHAR(50)",
    },
    "action_items": {
        "project_id": "INTEGER",
        "document_id": "INTEGER",
        "description": "TEXT",
        "owner": "VARCHAR(255)",
        "due_date": "VARCHAR(50)",
        "status": "VARCHAR(100)",
    },
    "risks": {
        "project_id": "INTEGER",
        "document_id": "INTEGER",
        "description": "TEXT",
        "impact": "TEXT",
        "mitigation": "TEXT",
        "owner": "VARCHAR(255)",
    },
    "timeline_events": {
        "project_id": "INTEGER",
        "source_document": "VARCHAR(255)",
        "event_date": "VARCHAR(50)",
        "title": "VARCHAR(255)",
        "description": "TEXT",
    },
    "jobs": {
        "project_id": "INTEGER",
        "document_id": "INTEGER",
        "filename": "VARCHAR(255)",
        "status": "VARCHAR(50)",
        "stage": "VARCHAR(100)",
        "progress": "INTEGER",
        "error_message": "TEXT",
        "created_at": "DATETIME",
        "updated_at": "DATETIME",
    },
}


def run_lightweight_migrations() -> None:
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table_name, columns in AUTO_MIGRATIONS.items():
            if not inspector.has_table(table_name):
                continue
            existing = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, column_type in columns.items():
                if column_name not in existing:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    run_lightweight_migrations()
