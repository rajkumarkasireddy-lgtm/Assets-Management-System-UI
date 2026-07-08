from typing import Optional, List
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.ticket import Ticket, TicketComment
from app.repositories.base import BaseRepository
import uuid

class TicketRepository(BaseRepository[Ticket]):
    def __init__(self):
        super().__init__(Ticket)

    async def get_by_display_id(self, db: AsyncSession, display_id: str) -> Optional[Ticket]:
        """Fetch active ticket by its display ID with loaded comments."""
        query = (
            select(Ticket)
            .where(Ticket.display_id == display_id, Ticket.is_active == True)
            .options(selectinload(Ticket.comments))
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_with_comments(self, db: AsyncSession, ticket_id: uuid.UUID) -> Optional[Ticket]:
        """Fetch active ticket by UUID with loaded comments."""
        query = (
            select(Ticket)
            .where(Ticket.id == ticket_id, Ticket.is_active == True)
            .options(selectinload(Ticket.comments))
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def create_comment(self, db: AsyncSession, ticket_id: uuid.UUID, author_name: str, message: str) -> TicketComment:
        """Create a comment on a ticket."""
        comment = TicketComment(
            ticket_id=ticket_id,
            author_name=author_name,
            message=message
        )
        db.add(comment)
        await db.flush()
        return comment

    async def count_pending(self, db: AsyncSession) -> int:
        """Count active tickets that are not resolved or closed."""
        query = (
            select(func.count(Ticket.id))
            .where(
                Ticket.is_active == True,
                Ticket.status != "Resolved",
                Ticket.status != "Closed"
            )
        )
        result = await db.execute(query)
        return result.scalar() or 0

ticket_repository = TicketRepository()
