from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Message
from app.schemas.message import MessageCreate, MessageUpdate, MessageStatus
from app.crud.CRUDMessage import crud_message


class MessageService:
    @staticmethod
    async def get_chat_messages(
        db: AsyncSession, chat_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        return await crud_message.get_by_chat_id(
            db, chat_id=chat_id, skip=skip, limit=limit
        )

    @staticmethod
    async def get_user_chat_messages(
        db: AsyncSession, chat_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        return await crud_message.get_by_chat_id_and_user(
            db, chat_id=chat_id, user_id=user_id, skip=skip, limit=limit
        )

    @staticmethod
    async def get_message(db: AsyncSession, message_id: int) -> Optional[Message]:
        return await crud_message.get(db, message_id)

    @staticmethod
    async def create_message(
        db: AsyncSession, message_create: MessageCreate, user_id: int
    ) -> Optional[Message]:
        return await crud_message.create_with_chat_check(
            db, obj_in=message_create, user_id=user_id
        )

    @staticmethod
    async def update_message(
        db: AsyncSession, message_id: int, message_update: MessageUpdate
    ) -> Optional[Message]:
        message = await crud_message.get(db, message_id)
        if message:
            return await crud_message.update(db, db_obj=message, obj_in=message_update)
        return None

    @staticmethod
    async def delete_message(db: AsyncSession, message_id: int) -> Optional[Message]:
        return await crud_message.remove(db, id=message_id)

    @staticmethod
    async def update_message_status(
        db: AsyncSession, message_id: int, status: MessageStatus
    ) -> Optional[Message]:
        return await crud_message.update_status(
            db, message_id=message_id, status=status
        )

    @staticmethod
    async def get_latest_messages(
        db: AsyncSession, chat_id: int, limit: int = 10
    ) -> List[Message]:
        return await crud_message.get_latest_by_chat_id(
            db, chat_id=chat_id, limit=limit
        )

    @staticmethod
    async def get_message_count(db: AsyncSession, chat_id: int) -> int:
        return await crud_message.get_count_by_chat_id(db, chat_id=chat_id)


message_service = MessageService()
