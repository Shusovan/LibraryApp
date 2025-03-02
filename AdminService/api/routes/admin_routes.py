from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.admin_schema import AdminCreate, AdminResponse
from services.admin_service import create_admin, get_admin_by_email, get_all_admins
from database.db_connection import get_db


router = APIRouter()

# Only SUPER_ADMIN can add ADMIN
@router.post("/add-admin/", response_model=AdminResponse)
def add_admin(admin_data: AdminCreate, request: Request, db: Session = Depends(get_db)):

    return create_admin(db, admin_data, request)


# find all admins from database
@router.get("/get-admins", response_model=list[AdminResponse])
def all_admins(db: Session = Depends(get_db)):
    
    return get_all_admins(db)


# get ADMIN by their email
@router.get("/admin/{email}", response_model=AdminResponse)
def find_admin_by_email(email: str, db: Session = Depends(get_db)):
    
    admin = get_admin_by_email(db, email)
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return admin