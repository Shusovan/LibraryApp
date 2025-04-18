import uuid
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from config.security_client import validate_token
from model.book import Book
from model.genre import Genre
from schema.book_schema import BookCreate


def create_book(db: Session, book_data: BookCreate, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService

    
    # Check if the user is LIBRARIAN
    if user_data.get("role") != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Forbidden: Only LIBRARIAN can add books")
    
    # Check if the same book already exists (by name and author)
    existing_book = db.query(Book).filter(
        Book.book_name == book_data.book_name,
        Book.author == book_data.author
    ).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    

    # book_id logic (generates automatically)
    short_uuid = str(uuid.uuid4()).replace("-", "")[:6]

    book = Book(book_id=short_uuid, book_name=book_data.book_name, book_description=book_data.book_description, author=book_data.author, available_copies=book_data.available_copies, catagory="NORMAL", created_by=user_data.get("id"), modified_by=user_data.get("id"))
    
    db.add(book)
    
    # Process each genre name
    genres_list = []
    for genre_name in book_data.genres:
        # Try to find existing genre
        genre = db.query(Genre).filter(Genre.name == genre_name).first()
        
        # If not found, create it
        if not genre:
            genre = Genre(name=genre_name)
            db.add(genre)
            db.flush()  # Get ID without committing yet
        
        genres_list.append(genre)
    
    # Link genres to book
    book.genres = genres_list

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


def update_availability(book_id: str, borrow_data: dict, db: Session):

    # extract status from payload
    status = borrow_data.get("status")

    if not status:
        raise HTTPException(status_code=400, detail="Status not provided")
    
    # find book by book id provided
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # borrow books
    if status == "BORROWED":
        
        if book.available_copies == 0:
            raise HTTPException(status_code=400, detail="No copies available to borrow")
        
        book.available_copies -= 1

    # return book
    elif status == "RETURNED":
        book.available_copies += 1

    else:
        raise HTTPException(status_code=400, detail="Invalid status.")

    db.commit()
    db.refresh(book)

    print("Updated Available Books:", book.available_copies)

    return {"available_copies": book.available_copies}