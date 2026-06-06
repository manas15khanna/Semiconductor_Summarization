from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(255), default="")
    status: Mapped[str] = mapped_column(String(100), default="")
    decision_date: Mapped[str] = mapped_column(String(50), default="")

    project = relationship("Project", back_populates="decisions")
    document = relationship("Document", back_populates="decisions")
