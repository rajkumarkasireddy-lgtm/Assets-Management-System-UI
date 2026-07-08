from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.services.dashboard import dashboard_service
from app.schemas.base import ApiResponse
from app.schemas.dashboard import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=ApiResponse[DashboardStats])
async def get_dashboard_statistics(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Aggregate metrics and activities for the platform dashboard."""
    stats = await dashboard_service.get_stats(db)
    return ApiResponse(
        success=True,
        message="Dashboard stats loaded",
        data=stats
    )
