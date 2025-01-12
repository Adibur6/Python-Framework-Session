from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from .base import Base

class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name}, email={self.email})>"
