from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey
from  src.models.base import Base

class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id"), nullable=False)
    room_id: Mapped[str] = mapped_column(String(50), ForeignKey("rooms.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="messages")
    room: Mapped["Room"] = relationship("Room", back_populates="messages")

    def __repr__(self):
        return f"<Message(user_id={self.user_id}, room_id={self.room_id}, content={self.content})>"
