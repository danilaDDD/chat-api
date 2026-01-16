import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.connection import create_session_factory
from db.session_manager import SessionManager


@pytest.fixture(scope="module")
def session_factory(settings) -> async_sessionmaker[AsyncSession]:
    return create_session_factory(settings)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_factory):
    async with session_factory() as session:
        await session.execute(text("DELETE FROM messages;"))
        await session.execute(text("DELETE FROM chats;"))
        await session.commit()
    yield