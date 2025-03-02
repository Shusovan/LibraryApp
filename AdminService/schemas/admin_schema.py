from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AdminCreate(BaseModel):
    name : str
    email : str
    password : str


class AdminResponse(BaseModel):
    id : UUID
    email : str
    password : str
    # created_by : UUID
    # modified_by : UUID
    created_date : datetime
    modified_date : datetime
    is_deleted : bool
    role_id : int

    class Config:
        from_attributes = True