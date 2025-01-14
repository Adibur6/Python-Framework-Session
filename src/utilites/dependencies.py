from typing import Annotated
from fastapi import Header
from fastapi.exceptions import HTTPException
from src.models import SessionAsync
from fastapi import Request
import uuid
import datetime
from typing import Optional
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
        
# in memory session storage
user_session = {}

def set_user_token(user, request, response):
    if request.cookies.get("token"):
        token = request.cookies.get("token")
        delete_user_token(token)
    token = str(uuid.uuid4())
    user_session[token] = {
        "user_id": user.id,
        "expires_in": datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    response.set_cookie("token", token)

    return {"token": token}

def delete_user_token(token):
    if token in user_session:
        del user_session[token]
        return True
    return False
    
    

async def authenticate_user(
    request: Request,
    x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token")
) -> str:
    token: Optional[str] = x_auth_token
    if not token:
        token = request.cookies.get("token")
    
    if not token or token not in user_session:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    session_data = user_session[token]
    if session_data["expires_in"] < datetime.datetime.now():
        raise HTTPException(status_code=401, detail="Token has expired")
    
    return session_data.get("user_id")