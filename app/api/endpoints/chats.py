from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.authentication.auth import current_active_user
from app.db.database import db_helper
from app.db.models import User
from app.schemas.chat import (
    ChatRead,
    ChatCreate,
    ChatUpdate,
)
from app.services.ChatService import chat_service

chats_router = APIRouter(prefix="/chats", tags=["chats"])


@chats_router.get("", response_model=List[ChatRead])
async def get_current_user_chats(
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of records to return"),
):
    """Получить все чаты текущего пользователя"""
    chats = await chat_service.get_user_chats(
        db, user_id=user.id, skip=skip, limit=limit
    )
    return chats


@chats_router.get("/{chat_id}", response_model=ChatRead)
async def get_chat(
    chat_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить информацию о конкретном чате"""
    chat = await chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    # Проверяем, что чат принадлежит пользователю
    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this chat",
        )

    return chat


@chats_router.post("", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_create: ChatCreate,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новый чат"""
    # Убеждаемся, что пользователь создает чат для себя
    if chat_create.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only create chats for yourself",
        )

    chat = await chat_service.create_chat(db, chat_create)
    return chat


@chats_router.put("/{chat_id}", response_model=ChatRead)
async def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить информацию о чате"""
    chat = await chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    # Проверяем, что чат принадлежит пользователю
    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this chat",
        )

    updated_chat = await chat_service.update_chat(db, chat_id, chat_update)
    if not updated_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found after update"
        )

    return updated_chat


@chats_router.patch("/{chat_id}/title", response_model=ChatRead)
async def update_chat_title(
    chat_id: int,
    title: Annotated[str, Body(..., embed=True, description="New chat title")],
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить только название чата"""
    chat = await chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this chat",
        )

    updated_chat = await chat_service.update_chat(db, chat_id, ChatUpdate(title=title))
    if not updated_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found after update"
        )

    return updated_chat


@chats_router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить чат"""
    chat = await chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this chat",
        )

    deleted_chat = await chat_service.delete_chat(db, chat_id)
    if not deleted_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found during deletion",
        )

    return None
