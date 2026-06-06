from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    document_id: Mapped[int | None] = mapped_column(ForeignKey("documents.id"), nullable=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(50), default="queued", index=True)
    stage: Mapped[str] = mapped_column(String(100), default="Upload Complete")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
    document = relationship("Document")
