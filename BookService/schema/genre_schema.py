from typing import List
from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str

class BulkGenreCreate(BaseModel):
    genres: List[GenreCreate]

class GenreResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True