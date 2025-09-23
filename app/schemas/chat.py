from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.message import MessageRead
from app.schemas.user import UserRead


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    user_id: int


class ChatUpdate(BaseModel):
    title: Optional[str] = None


class ChatInDBBase(ChatBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatRead(ChatInDBBase):
    pass


class ChatWithMessages(ChatInDBBase):
    messages: List[MessageRead] = []


class ChatWithUser(ChatInDBBase):
    user: UserRead


class ChatWithMessagesAndUser(ChatInDBBase):
    messages: List[MessageRead] = []
    user: UserRead
