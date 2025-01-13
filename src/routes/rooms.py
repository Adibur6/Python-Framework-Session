from fastapi import APIRouter, status, Depends, Security, HTTPException
from src.utilites.dependencies import authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.common import CommonFilters
from src.utilites.dependencies import get_db
router = APIRouter(prefix="/api/rooms", dependencies=[Security(authenticate_user)], tags=["rooms"])


@router.get("")
async def list_rooms(filters: CommonFilters, user_id: int = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    return {"user_id": user_id}
    
'''
- POST /api/rooms: Create new room login required
- GET /api/rooms: List rooms login required
- POST /api/rooms/{room_id}/messages: Post new messages   login required
- GET /api/rooms/{room_id}/messages: List room messages   
- DELETE /api/rooms/{room_id}/messages/{message_id}: Delete message (own/bonus: admin user deleting) 
- PATCH /api/rooms/{room_id}/messages/{message_id}: for updating a message

'''
@router.post("")
async def create_room(user_id: int = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    return {"message": "Create room"}

@router.post("/{room_id}/messages")
async def post_message(room_id: int, user_id: int = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    return {"message": "Post message"}

@router.get("/{room_id}/messages")
async def list_messages(filters: CommonFilters,room_id: int, user_id: int = Depends(authenticate_user),  session: AsyncSession = Depends(get_db)):
    return {"message": "List messages"}

@router.delete("/{room_id}/messages/{message_id}")
async def delete_message(room_id: int, message_id: int, user_id: int = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    return {"message": "Delete message"}

@router.patch("/{room_id}/messages/{message_id}")
async def update_message(room_id: int, message_id: int, user_id: int = Depends(authenticate_user), session: AsyncSession = Depends(get_db)):
    return {"message": "Update message"}