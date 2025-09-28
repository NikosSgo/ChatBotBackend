from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


class MessageStatus(str, Enum):
    SENDING = "sending"
    SENT = "sent"
    ERROR = "error"
    DELIVERED = "delivered"


class MessageSender(str, Enum):
    BOT = "bot"
    USER = "user"


class MessageBase(BaseModel):
    text: str
    chat_id: int


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    text: Optional[str] = None
    status: Optional[MessageStatus] = None


class MessageInDBBase(BaseModel):
    id: int
    text: str
    status: MessageStatus
    sender: MessageSender
    chat_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageRead(MessageInDBBase):
    pass
