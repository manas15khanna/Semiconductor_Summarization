from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="project", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="project", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEvent", back_populates="project", cascade="all, delete-orphan")
