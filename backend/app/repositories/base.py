import uuid
from typing import Generic, TypeVar, Optional, Type, Any, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Generic repository providing common database operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: uuid.UUID) -> Optional[ModelType]:
        """Fetch active record by UUID."""
        query = select(self.model).where(self.model.id == id, self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_raw(self, db: AsyncSession, id: uuid.UUID) -> Optional[ModelType]:
        """Fetch raw record by UUID regardless of activity status."""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        """Fetch all active records."""
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        """Create a new database entry."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Update an existing database entry."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: ModelType) -> ModelType:
        """Soft-delete a database entry by marking it inactive."""
        db_obj.is_active = False
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_paginated(
        self,
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        search: Optional[str] = None,
        search_fields: List[str] = [],
        filters: dict = {}
    ) -> Tuple[List[ModelType], int]:
        """Retrieve a list of paginated, sorted, searched, and filtered records."""
        query = select(self.model).where(self.model.is_active == True)
        
        # Apply filters
        for field, val in filters.items():
            if val is not None and hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == val)
                
        # Apply search
        if search and search_fields:
            search_clauses = []
            for field in search_fields:
                if hasattr(self.model, field):
                    search_clauses.append(getattr(self.model, field).ilike(f"%{search}%"))
            if search_clauses:
                query = query.where(or_(*search_clauses))
                
        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            col = getattr(self.model, sort_by)
            if sort_desc:
                query = query.order_by(col.desc())
            else:
                query = query.order_by(col.asc())
        else:
            if hasattr(self.model, "created_at"):
                query = query.order_by(self.model.created_at.desc())
            else:
                query = query.order_by(self.model.id.desc())
                
        # Count total matching rows
        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0
        
        # Apply pagination offsets
        query = query.offset((page - 1) * limit).limit(limit)
        result = await db.execute(query)
        items = list(result.scalars().all())
        
        return items, total
