from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    async def get_recent(self, db: AsyncSession, limit: int = 5) -> List[AuditLog]:
        """Fetch the most recent audit log entries."""
        query = select(AuditLog).where(AuditLog.is_active == True).order_by(AuditLog.created_at.desc()).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

audit_log_repository = AuditLogRepository()
