from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from config.security_client import validate_token
from schemas.admin_schema import AdminCreate, AdminResponse
from services.admin_service_impl import create_admin, get_admin_by_email, get_all_admins
from database.db_connection import get_db


router = APIRouter()


# Only SUPER_ADMIN can create ADMIN after successful authentication
# update this endpoint
#@router.post("/create-admin", response_model=AdminResponse)
#def create_new_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    
    #existing_admin = get_admin_by_email(db, admin.email)
    
    #if existing_admin:
        #raise HTTPException(status_code=400, detail="Admin already exists")
    
    #return create_admin(db, admin)


@router.post("/add-admin/", response_model=AdminResponse)
def add_admin(admin_data: AdminCreate, request: Request, db: Session = Depends(get_db)):
    
    auth_header = request.headers.get("Authorization")
    user_data = validate_token(auth_header)  # Call SecurityService

    # Check if the user is SUPER_ADMIN
    if user_data.get("role") != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden: Only SUPER_ADMIN can create admins")

    return create_admin(db, admin_data)


# find all admins from database
@router.get("/get-admins", response_model=list[AdminResponse])
def all_admins(db: Session = Depends(get_db)):
    
    # admins = db.query(Admin).all()
    #return [AdminResponse(id=admin.id, name=admin.name, email=admin.email, password=admin.password, role_id=admin.role_id) for admin in admins]
    return get_all_admins(db)


# get ADMIN by their email
@router.get("/admin/{email}", response_model=AdminResponse)
def find_admin_by_email(email: str, db: Session = Depends(get_db)):
    
    admin = get_admin_by_email(db, email)
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return admin