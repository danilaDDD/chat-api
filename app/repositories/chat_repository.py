from app.models.models import Chat
from app.repositories.base import BaseRepository


class ChatRepository(BaseRepository):
    model = Chat