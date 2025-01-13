from fastapi import APIRouter, status, Depends, Security, HTTPException
from src.utilites.dependencies import authenticate_user

router = APIRouter(prefix="/api/rooms", dependencies=[Security(authenticate_user)], tags=["rooms"])


@router.get("")
async def list_rooms(user_id: int = Depends(authenticate_user)):
    return {"user_id": user_id}
    
