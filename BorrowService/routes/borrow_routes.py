from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional

from core.db_connection import get_db
from view.borrow_view import approved_borrow, book_return, borrow, borrowed_books


router = APIRouter()


# borrow book after aspproval
@router.post("/borrow-book")
def borrow_book(request: Request, book_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''
    Borrow a book after approval from LIBRARIAN
    '''
    return borrow(request=request, book_id=book_id, db=db)


# request borrow approval
@router.put("/borrow-approved/{request_id}")
def borrow_approved(request_id: str, approval_data: dict, db: Session = Depends(get_db)):
    '''
    Updates status after borrow request is Approved
    '''
    return approved_borrow(request_id, approval_data, db)


# return borrowed books
@router.put("/return-book/{book_id}")
def return_book(request: Request, book_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''
    Return a book
    '''
    return book_return(request=request, book_id=book_id, db=db)


# get all borrowed books
@router.get("/get-borrowed-books")
def get_borrowed_books(request: Request, db: Session = Depends(get_db)):
    '''
    get details of borrowed book for an user
    '''
    return borrowed_books(request, db)