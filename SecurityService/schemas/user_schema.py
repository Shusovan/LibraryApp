from uuid import UUID
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role_id: int

class AdminResponse(UserBase):
    id : UUID
    email: str
    password: str
    role_id: int

class UserResponse(UserBase):
    # id : UUID
    user_id: int
    email: str
    password: str
    role_id: int

class UserLogin(UserBase):
    email: str
    password: str
