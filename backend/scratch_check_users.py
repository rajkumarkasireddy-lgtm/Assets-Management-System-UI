import asyncio
from sqlalchemy import select
from app.database import SessionLocal
from app.models.user import User

async def main():
    async with SessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        print(f"Total users in DB: {len(users)}")
        for u in users:
            print(f"- {u.display_id}: {u.name} ({u.email}), active={u.is_active}, role={u.role}")

if __name__ == "__main__":
    asyncio.run(main())
