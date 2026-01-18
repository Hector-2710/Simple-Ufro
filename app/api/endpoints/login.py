from app.services.auth_service import auth_service
from app.schemas.token import Token
from app.api.deps import SessionDep
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.post("/access-token", response_model=Token)
async def login_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    return await auth_service.login(session, identifier=form_data.username, password=form_data.password)
