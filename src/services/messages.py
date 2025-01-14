from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.models.message import Message
from src.schemas.message import MessageCreatePayload, MessageResponse
from src.schemas.common import CommonFilters
from src.models.user_room_association import user_room_association
class MessageService:

    async def create_message(self, session: AsyncSession, body: MessageCreatePayload, user_id: str, room_id: str):
        
        message_data = body.model_dump()
        if not message_data:
            return None
       

        stm = select(user_room_association).where(
            user_room_association.c.user_id == user_id,
            user_room_association.c.room_id == room_id
        )
        

        result = await session.execute(stm)
        is_user_in_room = result.scalar_one_or_none() is not None
        
        if not is_user_in_room:
            return None
        

        message = Message(**message_data, user_id=user_id, room_id=room_id)
        session.add(message)
        

        await session.commit()
        await session.refresh(message)
       
        return message

    async def list_messages(self, session: AsyncSession, filters: CommonFilters, room_id: str, user_id: str):
        stm = select(Message).where(Message.room_id == room_id).offset(filters.offset).limit(filters.page_size)
        if filters.sort_by:
            stm = stm.order_by(desc(filters.sort_by)) if filters.order == "desc" else stm.order_by(filters.sort_by)
        res = await session.execute(stm)
        messages = res.scalars().all()
        response = []
        for message in messages:
            response.append(MessageResponse(
                id=message.id,
                content=message.content,
                user_id=message.user_id,
                room_id=message.room_id,
                created_at=message.created_at
            ))
        return response

    async def delete_message(self, session: AsyncSession, message_id: str, user_id: str, room_id: str):
        stm = select(Message).where(Message.id == message_id, Message.user_id == user_id, Message.room_id == room_id)
        res = await session.execute(stm)
        message = res.scalar_one_or_none()
        if message is None:
            return None
        await session.delete(message)
        await session.commit()
        return message
    async def update_message(self, session: AsyncSession, message_id: str, body: MessageCreatePayload, user_id: str, room_id: str):
        stm = select(Message).where(Message.id == message_id, Message.user_id == user_id, Message.room_id == room_id)
        res = await session.execute(stm)
        message = res.scalar_one_or_none()
        if message is None:
            return None
        for key, value in body.model_dump().items():
            if value is not None:
                setattr(message, key, value)
        await session.commit()
        await session.refresh(message)
        return message
