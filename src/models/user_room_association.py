from sqlalchemy import Table, Column, Integer, ForeignKey
from  src.models.base import Base

user_room_association = Table(
    "user_room_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), primary_key=True),
)
