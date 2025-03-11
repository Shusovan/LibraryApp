import os

from dotenv import load_dotenv
from fastapi import HTTPException
import requests


load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


def fetch_user_role(id: int):
    
    response = requests.get(f"{USER_SERVICE_URL}/get-role/{id}")

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=404, detail="Role not found in UserService")