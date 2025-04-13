from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database.db_connection import get_db
from model.user import User
from schema.user_schema import ApproveUserRequest, UserCreate, UserLoginResponse, UserRegistrationResponse, UserResponse
from service.user_service import create_user, user_approved


router = APIRouter()


# Register new users
@router.post("/register-user/", response_model=UserRegistrationResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    return create_user(db, user_data)


# get user by their email id
@router.get("/get-user/{email}", response_model=Optional[UserResponse])
def get_user_by_email(email: str, db: Session = Depends(get_db)):

    return db.query(User).filter(User.email == email).first()


# internal api for fetching user credentials for generating JWT
@router.get("/get-user-details/{email}", response_model=Optional[UserLoginResponse])
def user_details(email: str, db: Session = Depends(get_db)):

    return db.query(User).filter(User.email == email).first()


# Updates the user’s status and assigns the generated 8-digit user ID.
@router.put("/users/approve/{email}")
def approve_user(email: str, user_data: dict, db: Session = Depends(get_db)):
    '''
    Updates the user’s status and assigns the generated 8-digit user ID.
    '''
    return user_approved(email, user_data, db)