from typing import TYPE_CHECKING
from app.db.models import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from app.db.mixins import IDMixin, TimestampMixin
from app.db.types.user_id import UserIdType
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IDMixin, TimestampMixin, SQLAlchemyBaseUserTable[UserIdType]):
    chats = relationship("Chat", back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
