import pytest
from starlette.testclient import TestClient

from app.models.models import Chat, Message
from db.session_manager import SessionManager
from test.testutils.asserts import assert_error_response


@pytest.mark.asyncio
@pytest.mark.e2e
class TestDeleteChatRequest:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, client: TestClient, session_manager: SessionManager):
        self.client = client
        self.session_manager = session_manager

    async def test_when_exist_chat_then_return_204_no_content_and_deleted(self):
        chat = Chat(title="test chat",
                    messages=[Message(text="test message"), Message(text="test message2")],)
        chat_id = await self.save_chat(chat)

        resp = self.do_request(chat_id)

        assert resp.status_code == 204

        async with self.session_manager.start_without_commit() as session_manager:
            assert len(await session_manager.chats.get_all()) == 0
            assert len(await session_manager.messages.get_all()) == 0

    async def test_when_not_exist_chat_then_return_404(self):
        resp = self.do_request(chat_id=999)
        assert_error_response(resp, 404)

    async def save_chat(self, chat: Chat):
        async with self.session_manager.start_with_commit() as session_manager:
            chat = await session_manager.chats.save(chat)
            return chat.id

    def do_request(self, chat_id: int):
        return self.client.delete(f"/chats/{chat_id}")

