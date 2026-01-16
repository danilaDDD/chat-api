from datetime import datetime

import pytest
from starlette.responses import Response
from starlette.testclient import TestClient

from db.session_manager import SessionManager


@pytest.mark.e2e
@pytest.mark.asyncio
class TestCreateChatRequest:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, client: TestClient, session_manager: SessionManager):
        self.url = "/chats/"
        self.client = client
        self.session_manager = session_manager
        yield


    async def test_when_valid_request_then_return_201_and_created_chat(self):
        valid_request = {"title": "test chat"}
        resp = self._do_request(valid_request)

        assert resp.status_code == 201

        resp_json = resp.json()
        assert resp_json.get("id") is not None and isinstance(resp_json["id"], int)
        assert resp_json["title"] == valid_request["title"]
        assert resp_json.get("created_at") is not None and isinstance(resp_json["created_at"], str)

        async with self.session_manager.start_without_commit() as session_manager:
            chats = await session_manager.chats.get_all()
            assert len(chats) == 1
            chat = chats[0]
            assert chat.id == resp_json["id"]
            assert chat.title == valid_request["title"]
            assert chat.created_at is not None and isinstance(chat.created_at, datetime)


    @pytest.mark.parametrize("request_json", [
        {},
        {"title": ""},
        {"title": None},
        {"title": 123},
        {"invalid_field": "test"}
    ])
    async def test_when_invalid_request_then_return_422(self, request_json):
        resp = self._do_request(request_json)
        assert resp.status_code == 422


    def _do_request(self, valid_request: dict) -> Response:
        return self.client.post(self.url, json=valid_request)

