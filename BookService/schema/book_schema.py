from datetime import datetime
from pydantic import BaseModel


class BookCreate(BaseModel):
    book_name : str
    book_description : str
    author : str
    available_copies : int


class BookResponse(BaseModel):
    book_id : str
    book_name : str
    book_description : str
    author : str
    available_copies : int
    # created_by : UUID
    # modified_by : UUID
    created_date : datetime
    modified_date : datetime
    is_deleted : bool

    class Config:
        from_attributes = True