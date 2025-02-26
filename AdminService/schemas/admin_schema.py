from datetime import datetime
from pydantic import BaseModel


class AdminCreate(BaseModel):
    name : str
    email : str
    password : str


class AdminResponse(BaseModel):
    id : int
    email : str
    password : str
    created_by : int
    modified_by : int
    created_date : datetime
    modified_date : datetime
    is_deleted : bool
    role_id : int

    class Config:
        orm_mode = True