from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignment import Assignment
from app.repositories.base import BaseRepository

class AssignmentRepository(BaseRepository[Assignment]):
    def __init__(self):
        super().__init__(Assignment)

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[Assignment]:
        """Fetch active assignment by its display ID."""
        query = select(Assignment).where(Assignment.display_id == display_id, Assignment.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def count_returned(self, db: AsyncSession) -> int:
        """Count total returned assignments."""
        query = select(func.count(Assignment.id)).where(Assignment.status == "Returned", Assignment.is_active == True)
        result = await db.execute(query)
        return result.scalar() or 0

assignment_repository = AssignmentRepository()
