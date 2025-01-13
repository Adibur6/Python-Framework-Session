from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import SessionAsync
import uuid
import datetime
security = HTTPBasic()

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
    
    
async def get_requesting_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        session: AsyncSession = Depends(get_db)):
    # TODO
    # find if any user exists in the database with email == credentials.username
    # check if user.password_hash == userservice.hash_password(credentials.password)
    # if true, return the user
    # else raise exception
    pass
