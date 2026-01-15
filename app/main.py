from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import select, text
from app.core.config import settings
from app.db.session import init_db, engine
import redis.asyncio as redis
# Import models to register them with metadata
from app.models import User, Subject, Grade, Schedule

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await init_db()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Next Gen University Intranet API"}

@app.get("/health")
async def health_check():
    # Check DB Connection
    db_status = "down"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "up"
    except Exception as e:
        print(f"DB Error: {e}")

    # Check Redis Connection
    redis_status = "down"
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        redis_status = "up"
    except Exception as e:
        print(f"Redis Error: {e}")

    return {
        "status": "ok",
        "database": db_status,
        "redis": redis_status,
        "version": "1.0.0"
    }
