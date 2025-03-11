from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    firstname : str
    lastname : str
    password : str

class UserResponse(UserBase):
    # id : int
    user_id : Optional[int] = None
    firstname : str
    lastname : str
    created_date : datetime
    #modified_date : datetime
    status : str
    # role: str

# for internal service communication
class UserLoginResponse(UserBase):
    password : str
    user_id : Optional[int] = None
    status : str
    role_id: int

# Only expecting a message field
class UserRegistrationResponse(BaseModel):
    message: str  

class UserLogin(UserBase):
    password: str

class ApproveUserRequest(BaseModel):
    user_id: int
    status: str
    verified_by: UUID  # Who approved the user (e.g., Librarian)