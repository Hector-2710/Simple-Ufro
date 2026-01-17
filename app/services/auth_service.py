from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import user_service
from app.core import security
from app.core.exceptions import InvalidCredentialsError, InactiveUserError
from app.schemas.token import Token

class AuthService:
    @staticmethod
    async def login(session: AsyncSession, email: str, password: str) -> Token:
        user = await user_service.get_by_email(session, email)
        if not user:
            raise InvalidCredentialsError()
        if not security.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        
        if not user.is_active:
            raise InactiveUserError()

        access_token_expires = timedelta(minutes=30)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )

auth_service = AuthService()
