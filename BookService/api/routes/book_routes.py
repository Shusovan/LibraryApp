from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database.db_connection import get_db
from schema.book_schema import BookCreate, BookResponse
from view.book_service import create_book, find_book_by_bookid, get_all_books, update_availability


router = APIRouter()


# Only LIBRARIAN can add Books
@router.post("/add-book", response_model=BookResponse)
def add_book(request: Request, book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Create/Add books to Library
    """
    return create_book(db, book_data, request)


# GET books from database, only LIBRARIAN, USER, GUEST can access (for now)
@router.get("/get-books", response_model=list[BookResponse])
def get_books(request: Request, db: Session = Depends(get_db)):
    """
    GET books from database
    """
    return get_all_books(db, request)


# GET books from database using book_id, only LIBRARIAN can access (for now)
@router.get("/get-book-by-bookid/{bookid}", response_model=BookResponse)
def get_book_by_bookid(bookid: str, request: Request, db: Session = Depends(get_db)):
    """
    GET book by ID
    """
    return find_book_by_bookid(bookid, db, request)


@router.put("/update-available-copies/{book_id}")
def update_available_copies(book_id: str, borrow_data: dict, db: Session = Depends(get_db)):
    """
    Update book availability
    """
    return update_availability(book_id, borrow_data, db)