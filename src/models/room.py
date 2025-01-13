from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List
from  src.models.base import Base

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_room_association",
        back_populates="rooms",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}, description={self.description})>"
