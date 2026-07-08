from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.core.security import create_access_token, decode_token
from app.models.user import User
from app.services.user import user_service, generate_temp_password, get_password_hash
from app.schemas.base import ApiResponse
from app.schemas.user import (
    UserLogin, TokenResponseData, UserResponse, 
    ChangePasswordRequest, ForceChangePasswordRequest, ResetPasswordRequest
)
from app.email.email import email_service
from jose import JWTError
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=ApiResponse[TokenResponseData])
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate email and password. Returns access and refresh tokens."""
    data = await user_service.authenticate(db, credentials)
    return ApiResponse(
        success=True,
        message="Authentication successful",
        data=data
    )

@router.post("/logout", response_model=ApiResponse[None])
async def logout(current_user: User = Depends(get_current_user)):
    """Logs the user out (clears token on client)."""
    return ApiResponse(
        success=True,
        message="Sign out successful"
    )

@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    """Fetch profile of current logged-in user."""
    return ApiResponse(
        success=True,
        message="Profile retrieved successfully",
        data=UserResponse.model_validate(current_user)
    )

@router.post("/change-password", response_model=ApiResponse[None])
async def change_password(
    request: ChangePasswordRequest, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Change credentials verifying current password."""
    await user_service.change_password(db, current_user, request.old_password, request.new_password)
    return ApiResponse(
        success=True,
        message="Password updated successfully"
    )

@router.post("/force-change-password", response_model=ApiResponse[None])
async def force_change_password(
    request: ForceChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Forced change of temporary password on first login."""
    await user_service.force_change_password(db, current_user, request.new_password)
    return ApiResponse(
        success=True,
        message="Temporary password replaced successfully. Welcome aboard!"
    )

@router.post("/forgot-password", response_model=ApiResponse[None])
async def forgot_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Forgot password flow. Generates temporary password and sends mail."""
    # Find user
    from app.repositories.user import user_repository
    user = await user_repository.get_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email is not registered")
        
    temp_pwd = generate_temp_password()
    user.password_hash = get_password_hash(temp_pwd)
    user.must_change_password = True
    db.add(user)
    await db.flush()
    
    # Send email
    await email_service.send_temporary_password_email(
        name=user.name,
        email=user.email,
        temp_password=temp_pwd,
        role=user.role,
        login_url="http://localhost:8080/login"
    )
    
    return ApiResponse(
        success=True,
        message="Reset instructions and temporary password dispatched"
    )

@router.post("/refresh", response_model=ApiResponse[Dict[str, str]])
async def refresh_token(payload: Dict[str, str], db: AsyncSession = Depends(get_db)):
    """Exchange active refresh token for a new access token."""
    refresh = payload.get("refresh_token")
    if not refresh:
        raise HTTPException(status_code=400, detail="Refresh token required")
        
    claims = decode_token(refresh)
    if not claims or claims.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
    user_id = claims.get("sub")
    access = create_access_token(subject=user_id)
    
    return ApiResponse(
        success=True,
        message="Access token refreshed",
        data={"access_token": access, "token_type": "bearer"}
    )
