from pydantic import BaseModel


class AdminCreate(BaseModel):
    name : str
    email : str
    password : str


class AdminResponse(BaseModel):
    email : str
    password : str
    role_id : int

    class Config:
        orm_mode = True