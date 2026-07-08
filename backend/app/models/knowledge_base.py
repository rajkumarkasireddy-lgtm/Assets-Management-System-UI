from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin

class KnowledgeBase(Base, TimestampMixin):
    __tablename__ = "knowledge_base"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., KB-100
    title: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    views: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
