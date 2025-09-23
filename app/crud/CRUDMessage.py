from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.crud.CRUDBase import CRUDBase
from app.db.models import Message, Chat
from app.schemas.message import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    async def get_by_chat_id(
        self, db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Получить все сообщения чата (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .filter(self.model.chat_id == chat_id)
            .order_by(desc(self.model.created_at))  # Новые сообщения сначала
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_chat_id_with_chat(
        self, db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Получить сообщения чата с информацией о чате (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .options(joinedload(self.model.chat))
            .filter(self.model.chat_id == chat_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_chat_id_and_user(
        self,
        db: AsyncSession,
        chat_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Message]:
        """Получить сообщения чата с проверкой владельца чата (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .join(self.model.chat)
            .filter(
                self.model.chat_id == chat_id,
                Chat.user_id == user_id,  # Проверяем, что чат принадлежит пользователю
            )
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_chat_check(
        self, db: AsyncSession, *, obj_in: MessageCreate, user_id: int
    ) -> Optional[Message]:
        """Создать сообщение с проверкой, что чат принадлежит пользователю (асинхронно)"""
        # Проверяем, что чат существует и принадлежит пользователю
        chat_result = await db.execute(
            select(Chat).filter(
                Chat.id == obj_in.chat_id, Chat.user_id == user_id)
        )
        chat = chat_result.scalar_one_or_none()

        if not chat:
            return None

        # Создаем сообщение
        return await self.create(db, obj_in=obj_in)

    async def update_status(
        self, db: AsyncSession, *, message_id: int, status: str
    ) -> Optional[Message]:
        """Обновить статус сообщения (асинхронно)"""
        message = await self.get(db, message_id)
        if not message:
            return None

        # Используем базовый метод update для изменения статуса
        return await self.update(db, db_obj=message, obj_in={"status": status})

    async def get_latest_by_chat_id(
        self, db: AsyncSession, chat_id: int, limit: int = 10
    ) -> List[Message]:
        """Получить последние сообщения чата (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .filter(self.model.chat_id == chat_id)
            .order_by(desc(self.model.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_count_by_chat_id(self, db: AsyncSession, chat_id: int) -> int:
        """Получить количество сообщений в чате (асинхронно)"""
        result = await db.execute(
            select(self.model).filter(self.model.chat_id == chat_id)
        )
        return len(result.scalars().all())


crud_message = CRUDMessage(Message)
