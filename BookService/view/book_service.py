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
    if user_data.get("role") != "LIBRARIAN" and user_data.get("role") != "USER":
        raise HTTPException(status_code=403, detail="Forbidden: Only LIBRARIAN can fetch all book details")

    return db.query(Book).all()


def find_book_by_bookid(bookid: str, db: Session, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService
    
    # Check if the user is LIBRARIAN
    if user_data.get("role") != "LIBRARIAN" and user_data.get("role") != "USER":
        raise HTTPException(status_code=403, detail="Forbidden: Only LIBRARIAN can fetch all book details")

    book = db.query(Book).filter(Book.book_id == bookid).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


def update_availability(book_id: str, db: Session):
    
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available")

    book.available_copies -= 1  # Correct way to decrement

    db.commit()
    db.refresh(book)

    print("Available Books:", book.available_copies)

    return {"Available Books": book.available_copies}