from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.crud.CRUDChat import crud_chat


class ChatService:
    @staticmethod
    async def get_user_chats(
        db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        return await crud_chat.get_by_user_id(
            db, user_id=user_id, skip=skip, limit=limit
        )

    @staticmethod
    async def get_chat(db: AsyncSession, chat_id: int) -> Optional[Chat]:
        return await crud_chat.get(db, chat_id)

    @staticmethod
    async def create_chat(db: AsyncSession, chat_create: ChatCreate) -> Chat:
        return await crud_chat.create_with_user(db, obj_in=chat_create)

    @staticmethod
    async def update_chat(
        db: AsyncSession, chat_id: int, chat_update: ChatUpdate
    ) -> Optional[Chat]:
        chat = await crud_chat.get(db, chat_id)
        if chat:
            return await crud_chat.update(db, db_obj=chat, obj_in=chat_update)
        return None

    @staticmethod
    async def delete_chat(db: AsyncSession, chat_id: int) -> Optional[Chat]:
        return await crud_chat.remove(db, id=chat_id)

    @staticmethod
    async def get_chat_with_messages(db: AsyncSession, chat_id: int) -> Optional[Chat]:
        return await crud_chat.get_with_messages(db, chat_id)

    @staticmethod
    async def get_user_chats_with_messages(
        db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        return await crud_chat.get_by_user_id_with_messages(
            db, user_id=user_id, skip=skip, limit=limit
        )


chat_service = ChatService()
