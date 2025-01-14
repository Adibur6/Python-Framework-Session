from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.models.room import Room
from src.schemas.room import RoomCreatePayload, RoomResponse
from src.schemas.common import CommonFilters

from src.models.user import User
class RoomService:
    async def create_room(self, session: AsyncSession, body: RoomCreatePayload, user_id: str):
        
        room_data = body.model_dump(exclude={'users'})
        
        
        
        room = Room(**room_data)
        room.owner_id = user_id
        
        users = list(body.users) if body.users else []
        users.append(user_id)
        
        resolved_users = []
        for user_id in users:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                resolved_users.append(user)
            else:
                return None
        
        room.users = resolved_users
        
        
        session.add(room)
        await session.commit()
        await session.refresh(room)
        
        response = RoomResponse(
            id=room.id,
            name=room.name,
            description=room.description,
            owner_id=room.owner_id,
            users=[user for user in users]
            
        )
        return response
    
    async def list_rooms(self, session: AsyncSession, filters: CommonFilters, user_id: str):
        stm = select(Room).where(Room.owner_id==user_id).offset(filters.offset).limit(filters.page_size).options(joinedload(Room.users))
        if filters.sort_by:
            stm = stm.order_by(desc(filters.sort_by)) if filters.order == "desc" else stm.order_by(filters.sort_by)
        res = await session.execute(statement=stm)
        rooms = res.unique().scalars().all()
        response = []
        
        for room in rooms:
            response.append(RoomResponse(
                id=room.id,
                name=room.name,
                description=room.description,
                owner_id=room.owner_id,
                users=[user.id for user in room.users]
                
            ))


        
        return response

    async def get_room_by_id(self, room_id: str, session: AsyncSession, user_id: str):
        stm = select(Room).where(Room.id == room_id and Room.owner_id == user_id).options(joinedload(Room.users))
        res = await session.execute(stm)
        room = res.unique().scalar_one_or_none()
        if room is None:
            return None
        response = RoomResponse(
            id=room.id,
            name=room.name,
            description=room.description,
            owner_id=room.owner_id,
            users=[user.id for user in room.users]
            
        )
        return response 

    async def delete_room(self, room_id: str, session: AsyncSession, user_id: str):
        stm = select(Room).where(Room.id == room_id, Room.owner_id == user_id)
        res = await session.execute(stm)
        room = res.scalar_one_or_none()
        
        if room is None:
            return None
        
        await session.delete(room)
        await session.commit()
        return room