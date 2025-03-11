
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests


load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


# fetch the user cedentials from UserService
def fetch_user(email: str):

    response = requests.get(f"{USER_SERVICE_URL}/get-user-details/{email}")

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=404, detail="User not found in AdminService")