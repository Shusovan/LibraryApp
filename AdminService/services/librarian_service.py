from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from config.security_client import validate_token
from models.admin import Admin
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