from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    firstname : str
    lastname : str
    password : str

class UserResponse(UserBase):
    # id : int
    # user_id : int
    firstname : str
    lastname : str
    created_date : datetime
    #modified_date : datetime
    # status : str
    # role_id: int

# Only expecting a message field
class UserRegistrationResponse(BaseModel):
    message: str  

class UserLogin(UserBase):
    password: str
