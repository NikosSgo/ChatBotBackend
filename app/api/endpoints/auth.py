from fastapi import APIRouter
from app.core.authentication.auth import fastapi_users
from app.api.dependencies.authentication import authentication_backend
from app.schemas.user import UserRead, UserCreate

auth_router = APIRouter(prefix="/auth", tags=["auth"])

auth_router.include_router(fastapi_users.get_auth_router(authentication_backend))

auth_router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))

auth_router.include_router(fastapi_users.get_verify_router(UserRead))

auth_router.include_router(fastapi_users.get_reset_password_router())
