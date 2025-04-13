from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from config.security_client import validate_token
from models.admin import Admin
from models.role import Role
from schemas.admin_schema import AdminCreate
from security.encrypt import hash_password


def create_admin(db: Session, admin_data: AdminCreate, request: Request):

    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService

    # Check if the user is SUPER_ADMIN
    if user_data.get("role") != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden: Only SUPER_ADMIN can create admins")


    hashed_password = hash_password(admin_data.password)

    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()


    if not admin_role:
        raise HTTPException(status_code=500, detail="ADMIN role not found")
    
    admin = Admin(name=admin_data.name, email=admin_data.email, password=hashed_password, created_by=user_data.get("id"), modified_by=user_data.get("id"), role_id=admin_role.id)
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin


def get_all_admins(db: Session):
    return db.query(Admin).all()


def get_admin_by_email(db: Session, email: str):

    return db.query(Admin).filter(Admin.email == email).first()