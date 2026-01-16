from datetime import datetime

from pydantic import BaseModel


class BaseResponseEntity(BaseModel):
    id: int
    created_at: datetime