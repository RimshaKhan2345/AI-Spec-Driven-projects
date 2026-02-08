from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid
from pydantic import field_validator


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = False


class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = False
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships to todos and conversations
    todos: list["Todo"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    email: str
    password: str = Field(min_length=8)  # Require minimum 8 characters for passwords

    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        return v


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TodoCreate(TodoBase):
    title: str = Field(min_length=1, max_length=100)


class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = None


class TodoRead(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Chat models
class ConversationBase(SQLModel):
    pass


class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=2000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=2000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: "Conversation" = Relationship(back_populates="messages")


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class MessageCreate(MessageBase):
    conversation_id: uuid.UUID
    role: str = Field(max_length=20)
    content: str = Field(max_length=2000)


class MessageRead(MessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    timestamp: datetime


# Reordering to handle forward reference
Todo.model_rebuild()
Conversation.model_rebuild()