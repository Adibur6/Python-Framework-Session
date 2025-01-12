from sqlalchemy.orm import mapped_column, Mapped , relationship
from sqlalchemy import String, ForeignKey
from typing import List
from .user import User
from .base import Base
from .message import Message

class Room(Base):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[int] = mapped_column(int, ForeignKey("users.id"), nullable=False)
    users: Mapped[List['User']] = relationship("User", back_populates="room")
    messages: Mapped[List['Message']] = relationship("Message", back_populates="room")

    def __repr__(self):
        return f"<Room(name={self.name}, description={self.description}, owner_id={self.owner_id})>"