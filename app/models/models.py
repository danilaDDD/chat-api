from typing import List

from sqlalchemy import Column, Text, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from app.models.base import AbsCreated, AbsId


class Chat(AbsId, AbsCreated):
    __tablename__ = "chats"

    title: str = Column(String(200), nullable=False)
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Chat: {self.title}>"


class Message(AbsId, AbsCreated):
    __tablename__ = 'messages'

    text: str = Column(Text, nullable=False)
    chat_id: int = Column(Integer, ForeignKey('chats.id'), nullable=False)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    def __repr__(self):
        return f"<Message: {self.text[:20]} in Chat ID {self.chat_id}>"
