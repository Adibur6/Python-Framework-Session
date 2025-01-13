from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer
from typing import List
from src.models.base import Base
from src.models.user_room_association import user_room_association

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)

    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        secondary="user_room_association",
        back_populates="users",
    )
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, email={self.email})>"
