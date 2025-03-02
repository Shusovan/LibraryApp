import uuid
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from config.security_client import validate_token
from model.book import Book
from schema.book_schema import BookCreate


def create_book(db: Session, book_data: BookCreate, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService

    
    # Check if the user is LIBRARIAN
    if user_data.get("role") != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Forbidden: Only LIBRARIAN can add books")
    

    # book_id logic (generates automatically)
    short_uuid = str(uuid.uuid4()).replace("-", "")[:6]


    book = Book(book_id=short_uuid, book_name=book_data.book_name, book_description=book_data.book_description, author=book_data.author, available_copies=book_data.available_copies, created_by=user_data.get("id"), modified_by=user_data.get("id"))
    
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book


def get_all_books(db: Session, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService
    
    # Check if the user is LIBRARIAN
    if user_data.get("role") != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Forbidden: Only LIBRARIAN can fetch all book details")

    return db.query(Book).all()
    