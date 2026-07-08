from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Fetch active user by email."""
        query = select(User).where(User.email == email, User.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email_raw(self, db: AsyncSession, email: str) -> Optional[User]:
        """Fetch user by email regardless of active status."""
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[User]:
        """Fetch active user by employee/display ID."""
        query = select(User).where(User.display_id == display_id, User.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def count_users(self, db: AsyncSession) -> int:
        """Count total users in the system (active and inactive) for display ID generation."""
        query = select(func.count(User.id))
        result = await db.execute(query)
        return result.scalar() or 0

    async def count_employees(self, db: AsyncSession) -> int:
        """Count active users with standard 'employee' role."""
        query = select(func.count(User.id)).where(User.role == "employee", User.is_active == True)
        result = await db.execute(query)
        return result.scalar() or 0

user_repository = UserRepository()
