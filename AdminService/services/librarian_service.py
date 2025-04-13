from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from config.security_client import validate_token
from config.borrow_client import borrow_approval_response
from models.admin import Admin
from models.borrow_approval_request import BorrowApprovalRequest
from models.role import Role
from schemas.librarian_schema import LibrarianCreate
from security.encrypt import hash_password


def create_librarian(db: Session, librarian_data: LibrarianCreate, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService

    # Check if the user is ADMIN
    if user_data.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden: Only ADMIN can create Librarians")


    hashed_password = hash_password(librarian_data.password)

    librarian_role = db.query(Role).filter(Role.name == "LIBRARIAN").first()


    if not librarian_role:
        raise HTTPException(status_code=500, detail="LIBRARIAN role not found")
    
    librarian = Admin(name=librarian_data.name, email=librarian_data.email, password=hashed_password, created_by=user_data.get("id"), modified_by=user_data.get("id"), role_id=librarian_role.id)
    
    db.add(librarian)
    db.commit()
    db.refresh(librarian)
    
    return librarian


def get_all_librarians(db: Session):
    
    return db.query(Admin).all()


def get_librarian_by_email(db: Session, email: str):

    librarian = db.query(Admin).filter(Admin.email == email).first()

    if not librarian:
        raise HTTPException(status_code=404, detail="Admin not found")

    return librarian


# Borrow request for approval
def borrow_request(borrow_payload: dict, db: Session):
    """
    Store the borrow request in AdminService for manual approval.
    """

    request_id = UUID(borrow_payload["request_id"])

    # Check if request_id already exists
    existing_record = db.query(BorrowApprovalRequest).filter(BorrowApprovalRequest.request_id == request_id).first()

    if existing_record:
        raise HTTPException(status_code=400, detail="Borrow request already exists")

    # add borrow approval request in database
    borrow_record = BorrowApprovalRequest(request_id = UUID(borrow_payload["request_id"]),
        user_id = borrow_payload["user_id"],
        book_id = borrow_payload["book_id"],
        approval_status = borrow_payload["status"])
    
    db.add(borrow_record)
    db.commit()
    db.refresh(borrow_record)

    return "MESSAGE : record added successfully"


# Approve borrow request
def borrow_approval(request_id: str, current_user: dict, db: Session):
    '''
    Approve borrow request
    '''

    # fetch ID of current logged-in Admin/Librarian
    current_user_id = current_user.get("id")

    fetch_borrowrecord = db.query(BorrowApprovalRequest).filter(BorrowApprovalRequest.request_id == request_id).first()

    if not fetch_borrowrecord:
        raise HTTPException(status_code=404, detail="record not found")
    
    if fetch_borrowrecord.approval_status != "PENDING":
        raise HTTPException(status_code=200, detail="Record is already approved")
    
    status = fetch_borrowrecord.approval_status = "APPROVED"
    approved_by = fetch_borrowrecord.approved_by = current_user_id

    # Update the existing borrow request
    fetch_borrowrecord.approval_status = "APPROVED"
    fetch_borrowrecord.approved_by = current_user_id
    fetch_borrowrecord.approved_date = datetime.now()

    # Commit changes to the database
    db.commit()
    db.refresh(fetch_borrowrecord)

    # Update borrow request in BorrowService
    success = borrow_approval_response(request_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to approve borrow request")


    return {"message": f"Request for User ID: {fetch_borrowrecord.user_id} has been approved."}