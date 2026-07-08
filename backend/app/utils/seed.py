import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.asset import Asset
from app.models.ticket import Ticket, TicketComment
from app.models.assignment import Assignment
from app.models.vendor import Vendor
from app.models.maintenance import Maintenance
from app.models.audit_log import AuditLog
from app.models.notification import Notification
from app.models.knowledge_base import KnowledgeBase

def fmt_date(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")

async def seed_db():
    print("Resetting database and seeding credentials...")
    async with SessionLocal() as db:
        # 1. Clear all existing records to ensure a completely fresh start
        await db.execute(delete(TicketComment))
        await db.execute(delete(Ticket))
        await db.execute(delete(Assignment))
        await db.execute(delete(Maintenance))
        await db.execute(delete(Asset))
        await db.execute(delete(Vendor))
        await db.execute(delete(AuditLog))
        await db.execute(delete(Notification))
        await db.execute(delete(KnowledgeBase))
        await db.execute(delete(User))
        
        # 2. Seed only the 4 core login accounts for testing each role
        pwd_hash = get_password_hash("demo1234")
        
        core_accounts = [
            {"name": "Admin User", "email": "admin@acmecorp.com", "role": "admin", "display_id": "EMP-999"}
        ]
        
        for acc in core_accounts:
            u = User(
                id=uuid.uuid4(),
                display_id=acc["display_id"],
                name=acc["name"],
                email=acc["email"],
                password_hash=pwd_hash,
                role=acc["role"],
                department="IT",
                designation="IT Specialist",
                manager="Director IT",
                location="HQ - New York",
                status="Active",
                avatar="".join([part[0] for part in acc["name"].split()])[:2],
                phone="+1 555-0199",
                join_date=fmt_date(datetime.utcnow() - timedelta(days=365)),
                must_change_password=False
            )
            db.add(u)
            
        await db.commit()
        print("Database cleared and core credentials successfully seeded!")

if __name__ == "__main__":
    asyncio.run(seed_db())
