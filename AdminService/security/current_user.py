import os
from dotenv import load_dotenv
from fastapi import HTTPException, Request, Security
import requests

from config.security_client import validate_token


load_dotenv()

# SecurityService URL (for inter-service communication)
SECURITY_SERVICE_URL = os.getenv("SECURITY_SERVICE_URL")


def get_current_user(request:Request):

    auth_header = request.headers.get("Authorization")

    user_data = validate_token(auth_header)

    if not user_data.get("id") or not user_data.get("role"):
        raise HTTPException(status_code=401, detail="Invalid token data")

    return user_data