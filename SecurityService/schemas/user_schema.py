from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class UserResponse(UserBase):
    id: int
    username: str
    role_name: str

class AssignRoleRequest(UserBase):
    username: str
    role_name: str    # Role name should be predefined in the `Role` table

    class Config:
        orm_mode = True
