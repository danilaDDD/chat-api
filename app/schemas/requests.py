from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class CreateMessageRequest(BaseModel):
    text: str = Field(min_length=1)