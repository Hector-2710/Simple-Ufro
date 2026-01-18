from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserCreate, UserUpdate, UserRead
from app.core import security
from app.core.exceptions import UserAlreadyExistsError

class UserService:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def create(session: AsyncSession, user_in: UserCreate) -> User:
        existing_email = await UserService.get_by_email(session, user_in.email)
        if existing_email:
            raise UserAlreadyExistsError(f"Email {user_in.email} already registered")
        
        existing_username = await UserService.get_by_username(session, user_in.username)
        if existing_username:
            raise UserAlreadyExistsError(f"Username {user_in.username} already taken")

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
