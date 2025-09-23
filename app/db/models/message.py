from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models import Base
from app.db.mixins import IDMixin, TimestampMixin
import enum

if TYPE_CHECKING:
    from app.db.models import Chat


class MessageStatus(enum.Enum):
    SENDING = "sending"
    SENT = "sent"
    ERROR = "error"
    DELIVERED = "delivered"


class MessageSender(enum.Enum):
    BOT = "bot"
    USER = "user"


class Message(Base, IDMixin, TimestampMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[MessageStatus] = mapped_column(Enum(MessageStatus), nullable=False)
    sender: Mapped[MessageSender] = mapped_column(Enum(MessageSender), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)

    # Relationship
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
