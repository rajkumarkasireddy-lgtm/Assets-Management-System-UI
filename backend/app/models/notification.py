from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.base import TimestampMixin
import uuid

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Null means global notification
    title: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, default="info")  # info, warning, success, danger
    time: Mapped[str] = mapped_column(String)  # time representation (e.g., "5m ago")
    unread: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
