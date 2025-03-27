from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional

from core.db_connection import get_db
from view.borrow_view import approved_borrow, borrow


router = APIRouter()


# borrow book after aspproval
@router.post("/borrow-book")
def borrow_book(request: Request, book_id: Optional[str] = None, db: Session = Depends(get_db)):
    '''
    Borrow a book after approval from LIBRARIAN
    '''
    return borrow(request=request, book_id=book_id, db=db)


@router.put("/borrow-approved/{request_id}")
def borrow_approved(request_id: str, approval_data: dict, db: Session = Depends(get_db)):
    '''
    Updates status after borrow request is Approved
    '''
    return approved_borrow(request_id, approval_data, db)