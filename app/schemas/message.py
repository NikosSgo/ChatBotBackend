import enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

from app.db.models.message import MessageSender, MessageStatus


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
