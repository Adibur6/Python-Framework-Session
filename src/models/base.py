from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, DateTime


db_url = "sqlite+aiosqlite:///mydb.db"
engine = create_async_engine(db_url, echo=True)

SessionAsync = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
