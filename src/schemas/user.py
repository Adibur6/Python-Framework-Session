from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserCreatePayload(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime

class UserUpdatePayload(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None  
    
class UserLoginPayload(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    token: str
