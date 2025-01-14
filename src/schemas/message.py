from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class MessageCreatePayload(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    user_id: str
    room_id: str
    content: str
    created_at: datetime