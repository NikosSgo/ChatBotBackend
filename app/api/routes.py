from fastapi import APIRouter
from .endpoints import auth_router, chats_router, messages_router, users_router

api_router = APIRouter()

api_router.include_router(auth_router)

api_router.include_router(chats_router)

api_router.include_router(messages_router)

api_router.include_router(users_router)
