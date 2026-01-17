from app.models.models import Message
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    model = Message