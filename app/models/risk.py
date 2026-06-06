from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Risk(Base):
    __tablename__ = "risks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    impact: Mapped[str] = mapped_column(Text, default="")
    mitigation: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(255), default="")

    project = relationship("Project", back_populates="risks")
    document = relationship("Document", back_populates="risks")
