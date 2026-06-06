from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    storage_path: Mapped[str] = mapped_column(String(500), default="")
    processing_status: Mapped[str] = mapped_column(String(50), default="queued", index=True)
    raw_text: Mapped[str] = mapped_column(Text, default="")

    project = relationship("Project", back_populates="documents")
    summaries = relationship("Summary", back_populates="document", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="document", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="document", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="document", cascade="all, delete-orphan")
