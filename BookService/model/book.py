from datetime import datetime
from sqlalchemy import UUID, Boolean, Column, DateTime, Integer, String
from database.db_connection import Base


class Book(Base):

    __tablename__ = "books"


    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(String, unique=True, index=True, nullable=False)
    
    book_name = Column(String, nullable=False)

    book_description = Column(String, nullable=True)

    author = Column(String, nullable=False)

    available_copies = Column(Integer, nullable=False)

    # genre = Column(String, nullable=False)

    # catagory = Column(String, nullable=False)           # NORMAL, EXCLUSIVE

    created_by = Column(UUID(as_uuid=True), nullable=False)

    modified_by = Column(UUID(as_uuid=True), nullable=False)

    created_date = Column(DateTime, default = datetime.now())

    modified_date = Column(DateTime, default = datetime.now())

    is_deleted = Column(Boolean, default = False)