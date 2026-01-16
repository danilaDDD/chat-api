import datetime

from fastapi import Depends

from app.models.models import Chat
from app.schemas.requests import CreateChatRequest, CreateMessageRequest
from app.schemas.responses import ChatResponse, MessageResponseEntity, ChatDetailsResponse
from app.services.base import BaseDBService
from db.session_manager import SessionManager, get_session_manager


class RestChatService(BaseDBService):
    async def create_chat(self, request: CreateChatRequest) -> ChatResponse:
        async with self.session_manager.start_with_commit() as session_manager:
            chat = Chat(**request.model_dump())
            saved_chat = await session_manager.chats.save(chat)

            return ChatResponse(id=saved_chat.id,
                                title=saved_chat.title,
                                created_at=saved_chat.created_at)

    async def create_chat_message(self, chat_id: int, request: CreateMessageRequest) -> MessageResponseEntity:
        return MessageResponseEntity(chat_id=chat_id, text=request.text, id=1)

    async def get_chat_details(self, chat_id: int) -> ChatDetailsResponse:
        return ChatDetailsResponse(id=1, title="test", messages=[])

    async def delete_chat(self, chat_id: int) -> ChatResponse:
        return ChatResponse(title="test", id=chat_id)


def get_rest_chat_service(session_manager: SessionManager = Depends(get_session_manager)) -> RestChatService:
    return RestChatService(session_manager=session_manager)
