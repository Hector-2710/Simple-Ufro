import uuid
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserCreate, UserUpdate, UserRead
from app.core import security
from app.core.exceptions import UserAlreadyExistsError
from app.core.cache import cache

class UserService:
    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        key = f"user:id:{user_id}"
        cached_data = await cache.get(key)
        if cached_data:
            return User.model_validate(cached_data)

        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()
        
        if user:
            await cache.set(key, user.model_dump(mode='json'), ttl=300)
        return user

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        key = f"user:email:{email}"
        cached_data = await cache.get(key)
        if cached_data:
            return User.model_validate(cached_data)

        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        
        if user:
            await cache.set(key, user.model_dump(mode='json'), ttl=300)
        return user

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> Optional[User]:
        key = f"user:username:{username}"
        cached_data = await cache.get(key)
        if cached_data:
            return User.model_validate(cached_data)

        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().first()
        
        if user:
            await cache.set(key, user.model_dump(mode='json'), ttl=300)
        return user

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
        # Invalidate old cache entries
        await cache.client.delete(f"user:email:{db_user.email}")
        await cache.client.delete(f"user:username:{db_user.username}")
        await cache.client.delete(f"user:id:{db_user.id}")

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
