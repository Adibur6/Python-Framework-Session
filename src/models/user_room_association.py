from sqlalchemy import Table, Column, ForeignKey, String
from  src.models.base import Base

user_room_association = Table(
    "user_room_association",
    Base.metadata,
    Column("user_id", String(50), ForeignKey("users.id",ondelete="CASCADE"), primary_key=True),
    Column("room_id", String(50), ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
    
)
