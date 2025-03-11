from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.admin_client import fetch_admin
from config.user_client import fetch_user
from database.db_connection import get_db
from schemas.token_schema import Token
from schemas.user_schema import AdminResponse, UserResponse


router=APIRouter()


# fetch Admin details from AdminService
@router.get("/get-admin/{email}", response_model=AdminResponse)
def get_admin(email: str):

    admin_data = fetch_admin(email)

    return admin_data


# fetch User details from UserService
@router.get("/get-user/{email}", response_model=UserResponse)
def get_user(email: str):

    user_data = fetch_user(email)

    return user_data