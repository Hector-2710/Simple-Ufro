from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db
from app.api.api import api_router
from app.core import exceptions
from app.api import handlers
from app.core.cache import cache
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await cache.connect()
    yield
    await cache.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    version="1.0.0"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(exceptions.UserAlreadyExistsError, handlers.user_already_exists_handler)
app.add_exception_handler(exceptions.InvalidCredentialsError, handlers.invalid_credentials_handler)
app.add_exception_handler(exceptions.UserNotFoundError, handlers.user_not_found_handler)
app.add_exception_handler(exceptions.InactiveUserError, handlers.inactive_user_handler)
app.add_exception_handler(exceptions.RateLimitError, handlers.rate_limit_handler)

app.include_router(api_router, prefix="/api/v1")

