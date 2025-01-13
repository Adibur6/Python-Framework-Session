from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserUpdatePayload, UserCreatePayload, UserLoginPayload
from src.schemas.common import CommonFilters

import bcrypt
class UserService:
    def hash_password(self, value) -> str:
        salt = bcrypt.gensalt()
        hash_value = bcrypt.hashpw(value.encode("utf-8"), salt)
        return hash_value.decode("utf-8")

    async def create_user(self, session: AsyncSession, body: UserCreatePayload):
        user_data = body.model_dump()
        user = User(**user_data)
        user.password_hash = self.hash_password(body.password)
        session.add(user)
        await session.commit()
        return user

    async def list_users(self, session: AsyncSession, filters: CommonFilters):
        stm = select(User).offset(filters.offset).limit(filters.page_size)
        if filters.sort_by:
            stm = stm.order_by(desc(filters.sort_by)) if filters.order == "desc" else stm.order_by(filters.sort_by)
        res = await session.execute(statement=stm)
        return res.scalars().all()

    async def get_user_by_id(self, user_id: str, session: AsyncSession):
        stm = select(User).where(User.id == user_id)
        res = await session.execute(stm)
        user = res.scalar_one_or_none()
        return user
    async def update_user(self, user_id: int, body: UserUpdatePayload, session: AsyncSession):
        user_data = body.model_dump()
   
        stm = select(User).where(User.id == user_id)
        res = await session.execute(stm)
        user = res.scalar_one_or_none()
        
        if user is None:
            return None
        for key, value in user_data.items():
            if value is not None:
                setattr(user, key, value)
        if body.password:
            user.password_hash = self.hash_password(body.password)
        
        await session.commit()
        session.refresh(user)
        
        return user
    async def check_login_user(self, session: AsyncSession, body: UserLoginPayload):
        stm = select(User).where(User.email == body.email)
        res = await session.execute(stm)
        user = res.scalar_one_or_none()
        if user is None:
            return None
        if bcrypt.checkpw(body.password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return user
        return None

