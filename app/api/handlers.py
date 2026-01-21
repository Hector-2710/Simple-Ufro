from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core import exceptions

async def user_already_exists_handler(request: Request, exc: exceptions.UserAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"The user with email {exc.email} already exists in the system"},
    )

async def invalid_credentials_handler(request: Request, exc: exceptions.InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Incorrect email or password"},
    )

async def user_not_found_handler(request: Request, exc: exceptions.UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"},
    )

async def inactive_user_handler(request: Request, exc: exceptions.InactiveUserError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Inactive user"},
    )

async def rate_limit_handler(request: Request, exc: exceptions.RateLimitError):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later."},
    )
