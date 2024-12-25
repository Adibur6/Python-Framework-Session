from fastapi import FastAPI
from src.routes.users import router as user_router
from src.routes.rooms import router as room_router


app = FastAPI()
app.include_router(user_router)
app.include_router(room_router)
