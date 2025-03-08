from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database.db_connection import SessionLocal, get_db
from model.user import User
from schema.user_schema import UserCreate, UserRegistrationResponse, UserResponse
from service.user_service import create_user


router = APIRouter()


# Register new users
@router.post("/register-user/", response_model=UserRegistrationResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    return create_user(db, user_data)


# get user by their email id
@router.get("/get-user/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):

    return db.query(User).filter(User.email == email).first()


# Updates the user’s status and assigns the generated 8-digit user ID.
@router.put("/users/approve/{email}")
def approve_user(email: str, user_data: dict):

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.user_id = user_data["user_id"]
    user.status = user_data["status"]
    user.verified_by = user_data["verified_by"]
    
    db.commit()
    db.refresh(user)

    return {f"message": "User approved successfully", "user_id": user.user_id}