from typing import List

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponseEntity


class ChatResponse(BaseResponseEntity):
    title: str


class MessageResponseEntity(BaseResponseEntity):
    text: str


class ChatDetailsResponse(BaseResponseEntity):
    title: str
    messages: List[MessageResponseEntity]

