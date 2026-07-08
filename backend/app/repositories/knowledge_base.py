from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge_base import KnowledgeBase
from app.repositories.base import BaseRepository

class KnowledgeBaseRepository(BaseRepository[KnowledgeBase]):
    def __init__(self):
        super().__init__(KnowledgeBase)

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[KnowledgeBase]:
        query = select(KnowledgeBase).where(KnowledgeBase.display_id == display_id, KnowledgeBase.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

knowledge_base_repository = KnowledgeBaseRepository()
