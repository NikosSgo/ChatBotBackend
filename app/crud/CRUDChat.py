from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.crud.CRUDBase import CRUDBase
from app.db.models import Chat
from app.schemas.chat import ChatCreate, ChatUpdate


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    async def get_by_user_id(
        self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        """Получить все чаты пользователя (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_with_messages(self, db: AsyncSession, chat_id: int) -> Optional[Chat]:
        """Получить чат с сообщениями (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .options(joinedload(self.model.messages))
            .filter(self.model.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def create_with_user(self, db: AsyncSession, *, obj_in: ChatCreate) -> Chat:
        """Создать чат для пользователя (асинхронно)"""
        return await self.create(db, obj_in=obj_in)

    async def get_by_user_id_with_messages(
        self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Chat]:
        """Получить чаты пользователя с сообщениями (асинхронно)"""
        result = await db.execute(
            select(self.model)
            .options(joinedload(self.model.messages))
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_title_and_user(
        self, db: AsyncSession, title: str, user_id: int
    ) -> Optional[Chat]:
        """Найти чат по названию и пользователю (асинхронно)"""
        result = await db.execute(
            select(self.model).filter(
                self.model.title == title, self.model.user_id == user_id
            )
        )
        return result.scalar_one_or_none()


crud_chat = CRUDChat(Chat)
