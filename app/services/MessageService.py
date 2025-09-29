# app/services/MessageService.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Message
from app.schemas.message import (
    MessageCreate,
    MessageUpdate,
    MessageStatus,
    MessageSender,
)
from app.crud.CRUDMessage import crud_message
from app.utils.yandex_gpt.YandexAgent import YandexAgent


class MessageService:
    def __init__(self):
        self.agent = YandexAgent()

    async def get_chat_messages(
        self, db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        return await crud_message.get_by_chat_id(
            db, chat_id=chat_id, skip=skip, limit=limit
        )

    async def get_user_chat_messages(
        self,
        db: AsyncSession,
        chat_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Message]:
        return await crud_message.get_by_chat_id_and_user(
            db, chat_id=chat_id, user_id=user_id, skip=skip, limit=limit
        )

    async def get_message(self, db: AsyncSession, message_id: int) -> Optional[Message]:
        return await crud_message.get(db, message_id)

    async def create_message(
        self, db: AsyncSession, message_create: MessageCreate, user_id: int
    ) -> Optional[Message]:
        user_message = await crud_message.create_with_chat_check(
            db, obj_in=message_create, user_id=user_id
        )

        if not user_message:
            return None

        await self._generate_ai_response(
            db, message_create.text, message_create.chat_id
        )

        return user_message

    async def _generate_ai_response(
        self, db: AsyncSession, user_message: str, chat_id: int
    ) -> Optional[Message]:
        """Генерирует ответ от нейросети и сохраняет в базу"""
        try:
            ai_response_text = await self.agent.async_call(user_message)

            ai_message = Message(
                text=ai_response_text,
                chat_id=chat_id,
                status=MessageStatus.DELIVERED,
                sender=MessageSender.BOT,
            )

            db.add(ai_message)
            await db.commit()
            await db.refresh(ai_message)
            return ai_message

        except Exception as e:
            # Логируем ошибку
            print(f"Error generating AI response: {e}")

            # Создаем сообщение об ошибке
            error_message = Message(
                text="Извините, произошла ошибка при генерации ответа",
                chat_id=chat_id,
                status=MessageStatus.ERROR,
                sender=MessageSender.BOT,
            )

            db.add(error_message)
            await db.commit()
            await db.refresh(error_message)
            return error_message

    async def update_message(
        self, db: AsyncSession, message_id: int, message_update: MessageUpdate
    ) -> Optional[Message]:
        message = await crud_message.get(db, message_id)
        if message:
            return await crud_message.update(db, db_obj=message, obj_in=message_update)
        return None

    async def delete_message(
        self, db: AsyncSession, message_id: int
    ) -> Optional[Message]:
        return await crud_message.remove(db, id=message_id)

    async def update_message_status(
        self, db: AsyncSession, message_id: int, status: MessageStatus
    ) -> Optional[Message]:
        return await crud_message.update_status(
            db, message_id=message_id, status=status
        )

    async def get_latest_messages(
        self, db: AsyncSession, chat_id: int, limit: int = 10
    ) -> List[Message]:
        return await crud_message.get_latest_by_chat_id(
            db, chat_id=chat_id, limit=limit
        )

    async def get_message_count(self, db: AsyncSession, chat_id: int) -> int:
        return await crud_message.get_count_by_chat_id(db, chat_id=chat_id)


message_service = MessageService()
