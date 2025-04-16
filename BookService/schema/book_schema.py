from datetime import datetime
from typing import List
from pydantic import BaseModel

from schema.genre_schema import GenreResponse


class BookCreate(BaseModel):
    book_name : str
    book_description : str
    author : str
    available_copies : int
    genres: List[str]


class BookResponse(BaseModel):
    book_id : str
    book_name : str
    book_description : str
    author : str
    available_copies : int
    genres: List[GenreResponse]
    catagory: str
    # created_by : UUID
    # modified_by : UUID
    created_date : datetime
    modified_date : datetime
    is_deleted : bool

    class Config:
        from_attributes = True