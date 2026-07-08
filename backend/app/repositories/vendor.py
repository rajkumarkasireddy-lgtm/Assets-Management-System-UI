from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vendor import Vendor
from app.repositories.base import BaseRepository

class VendorRepository(BaseRepository[Vendor]):
    def __init__(self):
        super().__init__(Vendor)

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[Vendor]:
        query = select(Vendor).where(Vendor.display_id == display_id, Vendor.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

vendor_repository = VendorRepository()
