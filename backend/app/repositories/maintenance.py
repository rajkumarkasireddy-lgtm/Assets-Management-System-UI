from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.maintenance import Maintenance
from app.repositories.base import BaseRepository

class MaintenanceRepository(BaseRepository[Maintenance]):
    def __init__(self):
        super().__init__(Maintenance)

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[Maintenance]:
        query = select(Maintenance).where(Maintenance.display_id == display_id, Maintenance.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

maintenance_repository = MaintenanceRepository()
