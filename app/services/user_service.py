from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserCreate, UserUpdate
from app.core import security

class UserService:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def authenticate(session: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await UserService.get_by_email(session, email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def create(session: AsyncSession, user_in: UserCreate) -> User:
        db_user = User.model_validate(user_in, update={"hashed_password": security.get_password_hash(user_in.password)})
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def update(session: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
        user_data = user_in.model_dump(exclude_unset=True)
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = security.get_password_hash(password)
            user_data["hashed_password"] = hashed_password
            del user_data["password"]
            
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

user_service = UserService()
