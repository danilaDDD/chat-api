import pytest

from app.models.models import Chat
from app.repositories.chat_repository import ChatRepository


@pytest.mark.asyncio
@pytest.mark.db
class TestChatRepository:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session_factory):
        self.session_factory = session_factory
        yield


    async def test_create_chat(self):
        async with self.session_factory() as session:
            chat_repo = ChatRepository(session)
            chat = Chat(title="Test Chat")

            saved_chat = await chat_repo.save(chat)
            assert saved_chat.id is not None
            assert saved_chat.title == chat.title
            assert saved_chat.created_at is not None

            await session.commit()