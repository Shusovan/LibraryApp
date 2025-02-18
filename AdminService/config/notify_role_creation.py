import requests
from config.admin_config import SECURITY_SERVICE_URL


def request_role_creation(username : str, role_name : str):
    
    """Notify SecurityService to create a role and assign it to an admin."""
    
    try:
        response = requests.post(f"{SECURITY_SERVICE_URL}/assign-role", json={"username": username,"role_name": role_name})
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}