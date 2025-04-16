from sqlalchemy import Column, ForeignKey, Integer
from database.db_connection import Base


class BookGenre(Base):

    __tablename__ = "book_genre"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)

    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=True)

    # Optional metadata fields
    # from datetime import datetime
    # created_at = Column(DateTime, default=datetime.utcnow)