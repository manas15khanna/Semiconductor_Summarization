from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ActionItem(Base):
    __tablename__ = "action_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(255), default="")
    due_date: Mapped[str] = mapped_column(String(50), default="")
    status: Mapped[str] = mapped_column(String(100), default="")

    project = relationship("Project", back_populates="action_items")
    document = relationship("Document", back_populates="action_items")
