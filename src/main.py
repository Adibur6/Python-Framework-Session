from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.models.base import engine, Base
from src.routes.users import router as user_router
from src.routes.rooms import router as room_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(room_router)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        