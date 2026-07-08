from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., EMP-1000
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)  # employee, support, asset_manager, admin
    
    # Employee Profile Details
    department: Mapped[str] = mapped_column(String, nullable=True)
    designation: Mapped[str] = mapped_column(String, nullable=True)
    manager: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="Active")  # Active, Inactive, On Leave
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    join_date: Mapped[str] = mapped_column(String, nullable=True)
    
    # First login security check
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    
    # Onboarding hardware allocation workflow details
    allocation_date: Mapped[str] = mapped_column(String, nullable=True)
    allocation_time: Mapped[str] = mapped_column(String, nullable=True)
    allocation_status: Mapped[str] = mapped_column(String, nullable=True)  # Awaiting Asset Verification, etc.
    required_asset_category: Mapped[str] = mapped_column(String, nullable=True)
    allocated_asset_details: Mapped[dict] = mapped_column(JSON, nullable=True)
    allocation_history: Mapped[list] = mapped_column(JSON, nullable=True)
    
    # Relationships
    assigned_assets = relationship(
        "Asset", 
        back_populates="assigned_to_user", 
        foreign_keys="Asset.assigned_to_id"
    )
    created_tickets = relationship(
        "Ticket", 
        back_populates="creator", 
        foreign_keys="Ticket.created_by_id"
    )
    assigned_tickets = relationship(
        "Ticket", 
        back_populates="assignee", 
        foreign_keys="Ticket.assignee_id"
    )
