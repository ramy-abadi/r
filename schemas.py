from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str
    timestamp: datetime

class MessageCreate(MessageBase):
    sender_id: int
    conversation_id: int

class Message(MessageBase):
    id: int
    sender_id: int
    conversation_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    name: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    users: List[User]
    messages: List[Message]

    class Config:
        orm_mode = True
