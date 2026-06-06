from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    source_document: Mapped[str] = mapped_column(String(255), default="")
    event_date: Mapped[str] = mapped_column(String(50), default="")
    title: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text, default="")

    project = relationship("Project", back_populates="timeline_events")
