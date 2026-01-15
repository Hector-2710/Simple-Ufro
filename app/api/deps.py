from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, select
from app.core import security
from app.core.config import settings
from app.db.session import get_session
from app.models.user import User
from app.schemas import TokenPayload

# Allow path to be configured/used in Docs
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/access-token"
)

async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check if user exists (Async)
    statement = select(User).where(User.id == token_data.sub)
    result = await session.execute(statement)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
