from datetime import datetime

import pytest
from starlette.testclient import TestClient
from fastapi import Response

from app.models.models import Chat, Message
from db.session_manager import SessionManager
from test.testutils.asserts import assert_error_response


@pytest.mark.asyncio
@pytest.mark.e2e
class TestGetChatDetailsRequest:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, client: TestClient, session_manager: SessionManager):
        self.client = client
        self.session_manager = session_manager
        yield

    async def test_when_exist_chat_then_return_200_and_chat_details(self):
        new_chat = Chat(title="test chat")
        chat_id = await self.save_chat(new_chat)

        resp = self.do_request(chat_id)
        assert resp.status_code == 200

        resp_json = resp.json()
        assert resp_json["id"] == chat_id
        assert resp_json["title"] == "test chat"
        assert len(resp_json["messages"]) == 0
        assert isinstance(resp_json["created_at"], str)

    async def test_when_exist_chat_with_3_messages_then_return_200_and_chat_details_with_messages(self):
        async with self.session_manager.start_with_commit() as session_manager:
            start_time = datetime.now()
            messages = []
            for i in range(3):
                time = start_time.replace(microsecond=start_time.microsecond + i)
                messages.append(Message(text=f"message {i+1}", created_at=time))
            chat = Chat(title="test chat", messages=messages)

            chat = await session_manager.chats.save(chat)
            chat_id = chat.id

        resp = self.do_request(chat_id)

        assert resp.status_code == 200
        json = resp.json()
        assert json["id"] == chat_id
        assert json["title"] == "test chat"
        assert len(json["messages"]) == 3

        msg1, msg2, msg3 = json["messages"]
        assert msg1["created_at"] < msg2["created_at"] < msg3["created_at"]

        for i, msg in enumerate([msg1, msg2, msg3], start=1):
            assert msg["text"] == f"message {i}"
            assert msg["id"] >= 0

    async def test_when_not_exist_chat_then_return_404(self):
        resp = self.do_request(chat_id=999)

        assert_error_response(resp, 404)


    def do_request(self, chat_id: int) -> Response:
        return self.client.get(f"/chats/{chat_id}/")

    async def save_chat(self, new_chat: Chat) -> int:
        async with self.session_manager.start_with_commit() as session_manager:
            chat = await session_manager.chats.save(new_chat)
            return chat.id

