from sqlalchemy import Sequence

from app.models.models import Message
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    model = Message

    async def get_by_chat_id_order_by_created_at(self, chat_id: int) -> Sequence[Message]:
        query = (self.select()
                 .filter_by(chat_id=chat_id)
                 .order_by(Message.created_at))

        return await self.get_list(query)