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