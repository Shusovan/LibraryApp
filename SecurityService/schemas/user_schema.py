import email
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role_id: int

class UserResponse(UserBase):
    id : int
    email: str
    password: str
    role_id: int

class UserLogin(UserBase):
    email: str
    password: str
