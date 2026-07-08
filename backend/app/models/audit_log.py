from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., LOG-0
    action: Mapped[str] = mapped_column(String)
    user: Mapped[str] = mapped_column(String)  # Name of user
    target: Mapped[str] = mapped_column(String)  # E.g., Ticket ID or Employee ID
    timestamp: Mapped[str] = mapped_column(String)
    ip: Mapped[str] = mapped_column(String)
