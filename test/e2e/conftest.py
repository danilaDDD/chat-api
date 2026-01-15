import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.testclient import TestClient

from app.main import app
from app.models.models import PrimaryToken
from app.services.jwt_token_service import JWTTokenService
from db.connection import create_session_factory
from db.session_manager import SessionManager


@pytest.fixture(scope="module")
def session_factory(settings) -> async_sessionmaker[AsyncSession]:
    return create_session_factory(settings)


@pytest_asyncio.fixture(scope="module")
async def session_manager(session_factory) -> SessionManager:
    return SessionManager(session_factory)


@pytest.fixture(scope="module")
def client(settings) -> TestClient:
    return TestClient(
        app,
        base_url="http://test",
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db_before_test(session_manager: SessionManager):
    yield