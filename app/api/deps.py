from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select
from app.core import security
from app.models.user import UserRead, User
from app.schemas.token import TokenPayload
from app.db.session import SessionDep
from typing import Annotated
from app.core.exceptions import InvalidCredentialsError
from app.services.user_service import user_service
import uuid

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/access-token")

async def get_current_user(session: SessionDep, token: str = Depends(reusable_oauth2)) -> UserRead:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if not token_data.sub:
            raise InvalidCredentialsError()
    except (InvalidTokenError, ValidationError, ValueError):
        raise InvalidCredentialsError()
    
    user = await user_service.get_by_id(session, uuid.UUID(token_data.sub))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

GetCurrentUser = Annotated[UserRead, Depends(get_current_user)]