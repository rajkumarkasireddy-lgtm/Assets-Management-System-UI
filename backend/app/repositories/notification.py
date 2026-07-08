from typing import List, Optional
from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification
from app.repositories.base import BaseRepository
import uuid

class NotificationRepository(BaseRepository[Notification]):
    def __init__(self):
        super().__init__(Notification)

    async def get_by_user(self, db: AsyncSession, user_id: uuid.UUID) -> List[Notification]:
        """Fetch notifications scoped to user or global ones, ordered by newest."""
        query = (
            select(Notification)
            .where(
                Notification.is_active == True,
                or_(Notification.user_id == user_id, Notification.user_id.is_(None))
            )
            .order_by(Notification.created_at.desc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def mark_all_read(self, db: AsyncSession, user_id: uuid.UUID) -> None:
        """Mark all notifications as read for a user."""
        query = (
            update(Notification)
            .where(
                Notification.is_active == True,
                or_(Notification.user_id == user_id, Notification.user_id.is_(None)),
                Notification.unread == True
            )
            .values(unread=False)
        )
        await db.execute(query)

notification_repository = NotificationRepository()
