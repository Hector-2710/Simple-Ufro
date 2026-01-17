from typing import Any
from fastapi import APIRouter
from app.api.deps import SessionDep, GetCurrentUser
from app.models.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = await user_service.create(session, user_in)
    return user

@router.get("/me", response_model=UserRead)
async def read_user_me(current_user: GetCurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_user_me(session: SessionDep, user_in: UserUpdate, current_user: GetCurrentUser) -> Any:
    """
    Update current user.
    """
    user = await user_service.update(session, current_user, user_in)
    return user
