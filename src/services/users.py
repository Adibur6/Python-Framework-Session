from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreatePayload
from src.models.user import User

class UserService:
    def hash_password(self, value) -> str:
        return f"#{value}#"

    async def create_user(self, session: AsyncSession, body: UserCreatePayload):
        body_dict = body.model_dump()
        del body_dict["password"]
        user = User(**body_dict)
        user.password_hash = self.hash_password(body.password)
        session.add(user)
        await session.flush()
        return user

    async def list_users(self):
        pass

    async def get_user_by_id(self, user_id: int):
        pass

