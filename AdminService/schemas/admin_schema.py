from pydantic import BaseModel


class AdminCreate(BaseModel):
    name : str
    username : str
    password : str


class AdminResponse(BaseModel):
    id : int
    name : str

    class Config:
        orm_mode = True