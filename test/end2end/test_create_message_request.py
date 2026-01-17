import pytest
from starlette.responses import Response
from starlette.testclient import TestClient

from app.models.models import Chat
from db.session_manager import SessionManager
from test.testutils.asserts import assert_error_response


@pytest.mark.asyncio
@pytest.mark.e2e
class TestCreateMessageRequest:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, client: TestClient, session_manager: SessionManager):
        self.client = client
        self.session_manager = session_manager
        self.chat = Chat(title="test")

    async def test_when_exist_chat_and_valid_data_then_return_201_and_created(self):
        chat_id = await self.save_chat()

        valid_data = {"text": "text"}
        resp = self.do_request(valid_data, chat_id)

        assert resp.status_code == 201

        resp_json = resp.json()
        assert "id" in resp_json and resp_json["id"] > 0
        assert resp_json["text"] == valid_data["text"]
        assert isinstance(resp_json["created_at"], str)

        async with self.session_manager.start_without_commit() as session_manager:
            chats = await session_manager.chats.get_all()
            assert len(chats) == 1
            chat = chats[0]
            assert chat is not None
            assert chat.id == chat_id

            messages = await session_manager.messages.get_all()
            assert len(messages) == 1
            message = messages[0]
            assert message.text == valid_data["text"]
            assert message.chat_id == chat_id

    async def test_when_not_exist_chat_then_return_404(self):
        valid_data = {"text": "text"}
        resp = self.do_request(valid_data, chat_id=999)

        assert_error_response(resp, 404)

    @pytest.mark.parametrize("invalid_data", [
        {},
        {"text": ""},
        {"text": None},
        {"text": 123},
        {"invalid_field": "test"}
    ])
    async def test_when_invalid_data_then_return_422(self, invalid_data):
        chat_id = await self.save_chat()
        resp = self.do_request(invalid_data, chat_id)

        assert_error_response(resp, 422)



    async def save_chat(self) -> int:
        async with self.session_manager.start_with_commit() as session_manager:
            chat =  await session_manager.chats.save(self.chat)
            return chat.id

    def do_request(self, valid_data: dict, chat_id: int) -> Response:
        url = f"/chats/{chat_id}/messages/"
        return self.client.post(url, json=valid_data)



