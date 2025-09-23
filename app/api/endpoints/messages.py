from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.authentication.auth import current_active_user
from app.db.database import db_helper
from app.db.models import User, Chat
from app.schemas.message import (
    MessageRead,
    MessageCreate,
    MessageUpdate,
)
from app.services.MessageService import message_service

messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.get("/chat/{chat_id}", response_model=List[MessageRead])
async def get_chat_messages(
    chat_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
    skip: int = Query(0, ge=0, description="Number of messages to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of messages to return"),
    order: str = Query(
        "desc", description="Order by creation time (asc/desc)"),
):
    """Получить все сообщения чата (только если чат принадлежит пользователю)"""
    messages = await message_service.get_user_chat_messages(
        db, chat_id=chat_id, user_id=user.id, skip=skip, limit=limit
    )

    # При необходимости изменить порядок
    if order == "asc":
        messages = sorted(messages, key=lambda x: x.created_at)

    return messages


@messages_router.get("/{message_id}", response_model=MessageRead)
async def get_message(
    message_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить конкретное сообщение"""
    message = await message_service.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    chat_result = await db.execute(
        select(Chat).filter(Chat.id == message.chat_id, Chat.user_id == user.id)
    )
    chat = chat_result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this message",
        )

    return message


@messages_router.post(
    "", response_model=MessageRead, status_code=status.HTTP_201_CREATED
)
async def create_message(
    message_create: MessageCreate,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Создать новое сообщение"""
    message = await message_service.create_message(db, message_create, user.id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found or you don't have access to it",
        )

    return message


@messages_router.put("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновить сообщение"""
    message = await message_service.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    # Проверяем, что сообщение принадлежит чату пользователя
    chat_result = await db.execute(
        select(Chat).filter(Chat.id == message.chat_id, Chat.user_id == user.id)
    )
    chat = chat_result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this message",
        )

    updated_message = await message_service.update_message(
        db, message_id, message_update
    )
    if not updated_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found after update",
        )

    return updated_message


@messages_router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Удалить сообщение"""
    message = await message_service.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )

    # Проверяем, что сообщение принадлежит чату пользователя
    chat_result = await db.execute(
        select(Chat).filter(Chat.id == message.chat_id, Chat.user_id == user.id)
    )
    chat = chat_result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this message",
        )

    deleted_message = await message_service.delete_message(db, message_id)
    if not deleted_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found during deletion",
        )

    return None


@messages_router.get("/chat/{chat_id}/latest", response_model=List[MessageRead])
async def get_latest_messages(
    chat_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
    limit: int = Query(
        10, ge=1, le=100, description="Number of latest messages to return"
    ),
):
    """Получить последние сообщения чата"""
    # Сначала проверяем доступ к чату
    chat_result = await db.execute(
        select(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id)
    )
    chat = chat_result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this chat",
        )

    messages = await message_service.get_latest_messages(
        db, chat_id=chat_id, limit=limit
    )
    return messages


@messages_router.get("/chat/{chat_id}/count", response_model=dict)
async def get_message_count(
    chat_id: int,
    user: Annotated[User, Depends(current_active_user)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """Получить количество сообщений в чате"""
    # Проверяем доступ к чату
    chat_result = await db.execute(
        select(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id)
    )
    chat = chat_result.scalar_one_or_none()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this chat",
        )

    count = await message_service.get_message_count(db, chat_id=chat_id)
    return {"chat_id": chat_id, "message_count": count}
