from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.db_connection import get_db
from schemas.token_schema import Token
from schemas.user_schema import UserLogin
from security.jwt_utils import verify_token
from services.auth_service import admin_login, user_login


router=APIRouter()


# Handles admin login and returns a JWT token. Expects JSON input instead of form data.
@router.post("/admin/login", response_model=Token)
def login_admin(login_data: UserLogin, db: Session = Depends(get_db)):

    token_response = admin_login(email=login_data.email, password=login_data.password)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response


# Handles user login and returns a JWT token. Expects JSON input instead of form data.
@router.post("/user/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):

    token_response = user_login(email=login_data.email, password=login_data.password)

    if not token_response:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token_response


# Verify JWT Token
@router.post("/authenticate-token")
def authenticate_token(request: Request):

    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing or invalid")

    token = auth_header.split("Bearer ")[-1]
    payload = verify_token(token)  # Call the existing function

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload