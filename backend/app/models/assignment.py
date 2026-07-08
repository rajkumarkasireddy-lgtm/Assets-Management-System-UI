from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.base import TimestampMixin
import uuid

class Assignment(Base, TimestampMixin):
    __tablename__ = "assignments"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., ASG-2000
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"))
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_date: Mapped[str] = mapped_column(String)
    return_date: Mapped[str] = mapped_column(String, nullable=True)
    expected_return: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="Active")  # Active, Returned, Transferred
    
    # Relationships
    asset = relationship("Asset", back_populates="assignments")
    employee = relationship("User")
