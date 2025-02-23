from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.admin_client import fetch_admin
from database.db_connection import get_db
from schemas.token_schema import Token
from schemas.user_schema import UserLogin, UserResponse
from services.auth_service import login_user


router=APIRouter()


# fetch Admin details from AdminService
@router.get("/get-admin/{email}", response_model=UserResponse)
def get_admin(email: str):

    admin_data = fetch_admin(email)

    return admin_data


"""
    Handles user login and returns a JWT token.

    Parameters:
    - form_data: OAuth2PasswordRequestForm (contains username & password)
    - db: Database session dependency

    Returns:
    - JWT access token on successful authentication

    Note : Use x-www-form-urlencoded format in Postman

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    token_response = login_user(email=form_data.username, password=form_data.password)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response"""


"""
    Handles user login and returns a JWT token.
    Expects JSON input instead of form data.
"""
@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):

    token_response = login_user(email=login_data.email, password=login_data.password)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response