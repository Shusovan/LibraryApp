from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database.db_connection import get_db
from schemas.librarian_schema import LibrarianCreate, LibrarianResponse
from services.librarian_service import create_librarian, get_all_librarians, get_librarian_by_email


router = APIRouter()


@router.post("/add-librarian/", response_model=LibrarianResponse)
def add_librarian(admin_data: LibrarianCreate, request: Request, db: Session = Depends(get_db)):

    return create_librarian(db, admin_data, request)


@router.get("/get-admins", response_model=list[LibrarianResponse])
def all_librarians(db: Session = Depends(get_db)):
    
    return get_all_librarians(db)


@router.get("/librarian/{email}", response_model=LibrarianResponse)
def find_librarian_by_email(email: str, db: Session = Depends(get_db)):
    
    return get_librarian_by_email(db, email)