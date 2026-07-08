from sqlalchemy import String, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.base import TimestampMixin
import uuid

class Maintenance(Base, TimestampMixin):
    __tablename__ = "maintenance"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., MNT-300
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"))
    engineer: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    resolution: Mapped[str] = mapped_column(Text)
    parts: Mapped[str] = mapped_column(String)
    cost: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="Scheduled")  # Completed, In Progress, Scheduled
    
    # Relationships
    asset = relationship("Asset", back_populates="maintenances")
