from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.base import TimestampMixin
import uuid

class Asset(Base, TimestampMixin):
    __tablename__ = "assets"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., AST-10000
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    manufacturer: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    serial: Mapped[str] = mapped_column(String, unique=True, index=True)
    purchase_date: Mapped[str] = mapped_column(String)
    warranty_expiry: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    
    assigned_to_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String)  # Assigned, Available, Maintenance, Retired
    cost: Mapped[float] = mapped_column(Float)
    
    # Relationships
    assigned_to_user = relationship(
        "User", 
        back_populates="assigned_assets", 
        foreign_keys=[assigned_to_id]
    )
    tickets = relationship("Ticket", back_populates="asset")
    maintenances = relationship("Maintenance", back_populates="asset")
    assignments = relationship("Assignment", back_populates="asset")
