from fastapi import HTTPException
from passlib.context import CryptContext

from config.admin_client import fetch_admin
from config.role_client import fetch_role
from security.jwt_utils import create_token


# Define password context globally for efficiency
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
    Verifies a plain password against a hashed password.
"""
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


"""
    Authenticates the user by verifying email and password.
    Fetches user details from AdminService and generates JWT.

    Returns:
        dict: JWT access token if authentication is successful.
"""
def authenticate_user(email: str, password: str):
    
    # Fetch admin credentials
    admin_data = fetch_admin(email)
    
    if not admin_data:
        raise HTTPException(status_code=404, detail="Admin not found")

    received_password = admin_data.get("password")
    role_id = admin_data.get("role_id")


    # Fetch role name using role_id
    role_data = fetch_role(role_id)
    
    if not role_data:
        raise HTTPException(status_code=404, detail="Role not found")
    
    role_name = role_data.get("name")


    # Verify password
    if not verify_password(password, received_password):
        raise HTTPException(status_code=401, detail="Invalid password")


    # Generate JWT token with user details
    access_token = create_token(data={"sub": email, "role": role_name})


    return {"access_token": access_token, "token_type": "bearer"}


"""
    Handles user login and returns a JWT token.
"""
def login_user(email: str, password: str):
    
    return authenticate_user(email, password)