from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, ForeignKey

from .base import Base

class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(int, ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(int, ForeignKey("rooms.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"<Message(user_id={self.user_id}, room_id={self.room_id}, content={self.content})>"