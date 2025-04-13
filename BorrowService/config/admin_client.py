import os
from dotenv import load_dotenv
import requests

load_dotenv()

ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL")


def borrow_approval_request(borrow_request_payload):

    # Attach the header
    # headers = {"Authorization": auth_header} 

    try:
        response = requests.post(f"{ADMIN_SERVICE_URL}/borrow-request", json=borrow_request_payload)
        
        if response.status_code == 200:
            return response.json()  # Return book details as a dictionary
        
        else:
            return None  # No book found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching borrow response: {e}")
        
        return None