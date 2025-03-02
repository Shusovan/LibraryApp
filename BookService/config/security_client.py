import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests


load_dotenv()

# SecurityService URL (for inter-service communication)
SECURITY_SERVICE_URL = os.getenv("SECURITY_SERVICE_URL")


# Request SecurityService for token verification
def validate_token(auth_header: str):

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    headers = {"Authorization": auth_header}
    response = requests.post(f"{SECURITY_SERVICE_URL}/authenticate-token", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid or expired token")

    return response.json()