from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.schemas.common import CommonFilters
from src.schemas.user import UserCreatePayload, UserResponse, UserUpdatePayload, UserLoginPayload, UserLoginResponse
from src.utilites.dependencies import get_db

from ..services.users import UserService
from fastapi import Request

router = APIRouter(prefix="/api/users")

user_service = UserService()

@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    try:
        return await user_service.list_users(session=session, filters=filters)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_users(body: UserCreatePayload, session: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create_user(session=session, body=body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: str, session: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.get_user_by_id(user_id=user_id, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: str, body: UserUpdatePayload, session: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.update_user(user_id=user_id, body=body, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login_user(request: Request,body: UserLoginPayload, session: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.login_user(session=session, body=body)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user_service.generate_token(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user():
    pass