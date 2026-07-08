from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin

class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"
    
    display_id: Mapped[str] = mapped_column(String, unique=True, index=True)  # e.g., VND-100
    name: Mapped[str] = mapped_column(String)
    contact: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="Active")  # Active, Inactive
    contract_end: Mapped[str] = mapped_column(String)
