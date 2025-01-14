from fastapi import APIRouter, status, Depends, Security, HTTPException
from src.utilites.dependencies import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.common import CommonFilters
from src.utilites.dependencies import get_db
from src.schemas.room import RoomCreatePayload, RoomResponse
from src.services.rooms import RoomService
from src.schemas.message import MessageCreatePayload, MessageResponse
from src.services.messages import MessageService
'''
- POST /api/rooms: Create new room login required
- GET /api/rooms: List rooms login required
- POST /api/rooms/{room_id}/messages: Post new messages   login required
- GET /api/rooms/{room_id}/messages: List room messages   
- DELETE /api/rooms/{room_id}/messages/{message_id}: Delete message (own/bonus: admin user deleting) 
- PATCH /api/rooms/{room_id}/messages/{message_id}: for updating a message

'''
router = APIRouter(prefix="/api/rooms", dependencies=[Security(authenticate_user)], tags=["rooms"])

room_service = RoomService()
message_service = MessageService()

@router.get("", response_model=list[RoomResponse], status_code=status.HTTP_200_OK)
async def list_rooms(filters: CommonFilters, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        return await room_service.list_rooms(session=session, filters=filters, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("", response_model=RoomResponse,status_code=status.HTTP_201_CREATED)
async def create_room(body: RoomCreatePayload,user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        room = await room_service.create_room(session=session, body=body, user_id=user_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return room
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
async def get_room_by_id(room_id: str, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        room = await room_service.get_room_by_id(room_id=room_id, session=session, user_id=user_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: str, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        room = await room_service.delete_room(room_id=room_id, session=session, user_id=user_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/{room_id}/messages",response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def post_message(body: MessageCreatePayload, room_id: str, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        message = await message_service.create_message(session=session, body=body, user_id=user_id, room_id=room_id)
        if message is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 

@router.get("/{room_id}/messages", response_model=list[MessageResponse], status_code=status.HTTP_200_OK)
async def list_messages(filters: CommonFilters,room_id: str, user_id: str = Depends(authenticate_user),  session: AsyncSession = Depends(get_db)):
    try:
        return await message_service.list_messages(session=session, filters=filters, room_id=room_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{room_id}/messages/{message_id}")
async def delete_message(room_id: str, message_id: str, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        message = await message_service.delete_message(session=session, message_id=message_id, user_id=user_id, room_id=room_id)
        if message is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{room_id}/messages/{message_id}")
async def update_message(body:MessageCreatePayload, room_id: str, message_id: str, user_id: str = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    try:
        message = await message_service.update_message(session=session, message_id=message_id, body=body, user_id=user_id, room_id=room_id)
        if message is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
