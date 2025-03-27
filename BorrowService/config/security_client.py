import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests


load_dotenv()

# SecurityService URL (for inter-service communication)
SECURITY_SERVICE_URL = os.getenv("SECURITY_SERVICE_URL")


def validate_token(auth_header: str):
    """
    Request SecurityService for token verification
    """

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    headers = {"Authorization": auth_header}

    try:
        response = requests.post(f"{SECURITY_SERVICE_URL}/authenticate-token", headers=headers, timeout=3)
        response.raise_for_status()  # Raises an error for non-2xx responses

    except HTTPException as e:
        print(f"Exception during request:: {e}")
        return {}

    except requests.RequestException as e:
        print(f"Security Service request failed: {str(e)}")
        return {}

    return response.json()