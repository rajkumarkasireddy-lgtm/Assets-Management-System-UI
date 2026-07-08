import uuid
from datetime import datetime
from sqlalchemy import DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class TimestampMixin:
    """Mixin class for common fields on models: UUID id, timestamps, is_active flag."""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        server_default="true"
    )
