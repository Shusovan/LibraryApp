from sqlalchemy import Column, Integer, String
from database.db_connection import Base
from sqlalchemy.orm import relationship

from model.book_genre import BookGenre


class Genre(Base):

    __tablename__ = "genres"


    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True)


    books = relationship("Book", secondary=BookGenre.__tablename__, back_populates="genres")