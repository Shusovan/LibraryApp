import os
from dotenv import load_dotenv
import requests

load_dotenv()

# UserService URL (for inter-service communication)
BORROW_SERVICE_URL = os.getenv("BORROW_SERVICE_URL")


def borrow_approval_response(request_id):

    try:
        response = requests.put(f"{BORROW_SERVICE_URL}/borrow-approved/{request_id}", json={"status": "BORROWED"},)
        # return response.status_code == 200
        if response.status_code == 200:
            return response.json()  # Return book details as a dictionary
        
        else:
            return None  # No book found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching borrow response: {e}")
        return None