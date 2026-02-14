from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """Get current user info"""
    return current_user

@router.get("/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user)
):
    """Get user dashboard data"""
    # ... dashboard logic
    pass