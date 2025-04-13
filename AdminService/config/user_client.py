import os
from dotenv import load_dotenv
import requests

load_dotenv()

# UserService URL (for inter-service communication)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


# Calls UserService to update user status and assign an 8-digit user ID.
def user_approved_response(email, user_id, current_user_id):

    try:
        response = requests.put(f"{USER_SERVICE_URL}/users/approve/{email}", json={"user_id": user_id, "status": "ACTIVE", "verified_by": current_user_id},)

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False