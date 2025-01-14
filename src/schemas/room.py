from pydantic import BaseModel
from typing import Optional

class RoomCreatePayload(BaseModel):
    name: str
    description: str
    users: Optional[list[str]] = None

class RoomResponse(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str
    users: Optional[list[str]] = None

    


