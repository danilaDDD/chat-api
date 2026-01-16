from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.schemas.requests import CreateChatRequest, CreateMessageRequest
from app.schemas.responses import ChatResponse, MessageResponseEntity, ChatDetailsResponse
from app.services import rest_chat_service
from app.services.rest_chat_service import get_rest_chat_service, RestChatService

chat_router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

@chat_router.post("/",
                  responses={
                      HTTP_201_CREATED:{
                          "model": ChatResponse,
                          "description": "Chat created successfully."
                      }
                  })
async def create_chat(
        request: CreateChatRequest,
        rest_chat_service: RestChatService = Depends(get_rest_chat_service)) -> ChatResponse:
    return await rest_chat_service.create_chat(request)


@chat_router.post("/{chat_id}/messages",
                  responses={
                      201:{
                          "model": MessageResponseEntity,
                          "description": "Message created successfully."
                      }
                  })
async def create_chat_message(
        chat_id: int,
        request: CreateMessageRequest,
        rest_chat_service: RestChatService = Depends(get_rest_chat_service)) -> MessageResponseEntity:
    return await rest_chat_service.create_chat_message(chat_id, request)


@chat_router.get("/{chat_id}/",
                 responses={
                     200:{
                         "model": List[MessageResponseEntity],
                         "description": "List of messages in the chat."
                     },
                     404:{
                         "description": "Chat not found."
                     },
                 })
async def get_chat_details(chat_id: int,
                           rest_chat_service: RestChatService = Depends(get_rest_chat_service)) -> ChatDetailsResponse:
    return await rest_chat_service.get_chat_details(chat_id)

@chat_router.delete("/{chat_id}/",
                    responses={
                        204: {
                            "description": "Chat deleted successfully."
                        },
                        404: {
                            "description": "Chat not found."
                        }}
                    )
async def delete_chat(chat_id: int,
                      rest_chat_service: RestChatService = Depends(get_rest_chat_service)) -> None:
    await rest_chat_service.delete_chat(chat_id)


