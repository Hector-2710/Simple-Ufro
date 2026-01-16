from app.services.user_service import user_service
from app.core import security
from app.schemas.token import Token
from app.api.deps import SessionDep
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.post("/access-token", response_model=Token)
async def login_access_token(session: SessionDep,form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await user_service.authenticate(session, email=form_data.username, password=form_data.password)
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=30)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }
    