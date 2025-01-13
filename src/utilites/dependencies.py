from typing import Annotated
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import HTTPException
from src.models import SessionAsync
import uuid
import datetime
bearer_scheme = HTTPBearer()

async def get_db():
    session =  SessionAsync()
    try:
        yield session
    except:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()

user_session = {}

def set_user_token(user):
    token = str(uuid.uuid4())
    user_session[token] = {
        "user_id": user.id,
        "expires_in": datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    return {"token": token}

def delete_user_token(token):
    if token in user_session:
        del user_session[token]
        return True
    return False
    
    

async def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> int:
    token = credentials.credentials
    if token not in user_session or user_session[token]["expires_in"] < datetime.datetime.now():
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return user_session[token].get("user_id")