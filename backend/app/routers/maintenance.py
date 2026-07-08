from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user, RoleChecker
from app.models.user import User
from app.repositories.maintenance import maintenance_repository
from app.schemas.base import ApiResponse, PaginatedData
from app.schemas.maintenance import MaintenanceResponse, MaintenanceCreate
from typing import Optional

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.get("", response_model=ApiResponse[PaginatedData[MaintenanceResponse]])
async def list_maintenance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1, le=10000),
    sort_by: Optional[str] = Query(None),
    sort_desc: bool = Query(False),
    status_filter: Optional[str] = Query(None, alias="status")
):
    """Retrieve maintenance logs."""
    filters = {}
    if status_filter:
        filters["status"] = status_filter
        
    items, total = await maintenance_repository.get_multi_paginated(
        db, page=page, limit=limit, sort_by=sort_by, sort_desc=sort_desc,
        filters=filters
    )
    
    schemas = [MaintenanceResponse.model_validate(item) for item in items]
    
    return ApiResponse(
        success=True,
        message="Maintenance logs retrieved",
        data=PaginatedData(
            items=schemas,
            total=total,
            page=page,
            limit=limit
        )
    )

@router.post("", response_model=ApiResponse[MaintenanceResponse])
async def schedule_maintenance(
    maint_in: MaintenanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "support", "asset_manager"]))
):
    """Create or schedule maintenance for an asset. Support/Asset Manager/Admin only."""
    count = len(await maintenance_repository.get_all(db))
    display_id = f"MNT-{300 + count}"
    
    maint_data = maint_in.model_dump()
    maint_data.update({"display_id": display_id})
    
    maint = await maintenance_repository.create(db, maint_data)
    
    return ApiResponse(
        success=True,
        message="Maintenance event logged successfully",
        data=MaintenanceResponse.model_validate(maint)
    )
