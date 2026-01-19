import os
os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:pass@localhost/db"
os.environ["REDIS_URL"] = "redis://localhost:6379"
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.main import app as fastapi_app
from app.db.session import get_session
from app.core.cache import cache
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, future=True)

async_session_test = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    yield res
    res.close()

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

async def override_get_session() -> AsyncSession:
    async with async_session_test() as session:
        yield session

fastapi_app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(autouse=True)
async def mock_redis():
    cache.connect = AsyncMock()
    cache.close = AsyncMock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock()
    yield

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    async with async_session_test() as session:
        yield session
