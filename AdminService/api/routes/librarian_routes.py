from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import random

from config.user_client import user_approved_response
from database.db_connection import get_db
from schemas.librarian_schema import LibrarianCreate, LibrarianResponse
from security.current_user import get_current_user
from services.librarian_service import borrow_approval, borrow_request, create_librarian, get_all_librarians, get_librarian_by_email


router = APIRouter()


# Add librarians
@router.post("/add-librarian/", response_model=LibrarianResponse)
def add_librarian(admin_data: LibrarianCreate, request: Request, db: Session = Depends(get_db)):

    return create_librarian(db, admin_data, request)


@router.get("/get-admins", response_model=list[LibrarianResponse])
def all_librarians(db: Session = Depends(get_db)):
    
    return get_all_librarians(db)


# get librarian by email
@router.get("/librarian/{email}", response_model=LibrarianResponse)
def find_librarian_by_email(email: str, db: Session = Depends(get_db)):
    
    return get_librarian_by_email(db, email)


# testing 
@router.get("/get-current-librarian")
def find_current_librarian(librarian: dict = Depends(get_current_user)):

    return {"data": "This is protected data", "user": librarian}


# Librarians can approve users. This will assign an 8-digit user_id.
@router.post("/approve-user/{email}")
def approve_user(email: str, current_user: dict = Depends(get_current_user)):

    current_user_id = current_user.get("id")

    if current_user["role"] != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Only librarians can approve users")

    # Generate a random 8-digit user ID
    user_id = random.randint(10000000, 99999999)

    # Update the user status in UserService
    success = user_approved_response(email, user_id, current_user_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to approve user")


    return {"message": f"User {email} approved with new User ID: {user_id}"}


# Book borrow request
@router.post("/borrow-request")
def request_borrow(borrow_payload: dict, db: Session = Depends(get_db)):
    '''
    Internal API for storing book borrow requests by users
    '''
    return borrow_request(borrow_payload, db);


# Book borrow approval
@router.put("/approve-borrow/{request_id}")
def approve_borrow(request_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    Approve book borrow requested by user
    '''

    if current_user["role"] != "LIBRARIAN":
        raise HTTPException(status_code=403, detail="Only librarians can approve users")
    
    return borrow_approval(request_id, current_user, db)