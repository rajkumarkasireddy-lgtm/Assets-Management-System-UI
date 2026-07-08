from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.asset import Asset
from app.repositories.base import BaseRepository

class AssetRepository(BaseRepository[Asset]):
    def __init__(self):
        super().__init__(Asset)

    async def get_by_serial(self, db: AsyncSession, serial: str) -> Optional[Asset]:
        """Fetch active asset by serial number."""
        query = select(Asset).where(Asset.serial == serial, Asset.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[Asset]:
        """Fetch active asset by display/asset ID."""
        query = select(Asset).where(Asset.display_id == display_id, Asset.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def count_total(self, db: AsyncSession) -> int:
        """Count all assets (active and inactive) for display ID generation."""
        query = select(func.count(Asset.id))
        result = await db.execute(query)
        return result.scalar() or 0

    async def count_by_status(self, db: AsyncSession, status: str) -> int:
        """Count active assets by status (e.g. Assigned, Available)."""
        query = select(func.count(Asset.id)).where(Asset.status == status, Asset.is_active == True)
        result = await db.execute(query)
        return result.scalar() or 0

asset_repository = AssetRepository()
