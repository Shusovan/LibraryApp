from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.admin_schema import AdminCreate, AdminResponse
from services.admin_service_impl import create_admin, get_admin_by_username
from database.db_connection import get_db

router = APIRouter()

@router.post("/create-admin", response_model=AdminResponse)
def create_new_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    
    existing_admin = get_admin_by_username(db, admin.username)
    
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    return create_admin(db, admin)

'''
@router.get("/get-all-admins", response_model=list[AdminResponse])
def get_all_admins(db: Session = Depends(get_db)):
    return get_admins(db)'''
