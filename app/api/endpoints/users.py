from typing import Any
from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep, GetCurrentUser
from app.models.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    user = await user_service.get_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    
    user = await user_service.create(session, user_in)
    return user

@router.get("/me", response_model=UserRead)
async def read_user_me(current_user: GetCurrentUser) -> Any:
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_user_me(session: SessionDep, user_in: UserUpdate, current_user: GetCurrentUser) -> Any:
    user = await user_service.update(session, current_user, user_in)
    return user
