import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv


load_dotenv()

ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL")


# fetch the admin cedentials from AdminService
def fetch_admin(email: str):

    response = requests.get(f"{ADMIN_SERVICE_URL}/admin/{email}")

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=404, detail="User not found in AdminService")