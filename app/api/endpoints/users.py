from fastapi import APIRouter

from app.core.authentication.auth import fastapi_users
from app.schemas.user import (
    UserRead,
    UserUpdate,
)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

users_router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
