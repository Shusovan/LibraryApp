from fastapi import HTTPException
from passlib.context import CryptContext

from config.admin_client import fetch_admin
from config.role_client import fetch_role
from config.user_client import fetch_user
from config.user_role_client import fetch_user_role
from security.jwt_utils import create_token


# Create a password hashing context with Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

"""
    Verifies a plain password against a hashed password.
"""
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


"""
    Authenticates the admin by verifying email and password.
    Fetches admin details from AdminService and generates JWT.

    Returns:
        dict: JWT access token if authentication is successful.
"""
def authenticate_admin(email: str, password: str):
    
    # Fetch admin data
    admin_data = fetch_admin(email)
    
    if not admin_data:
        raise HTTPException(status_code=404, detail="Admin not found")

    # extract the admin credentials required for authentication
    stored_password = admin_data.get("password")
    role_id = admin_data.get("role_id")
    admin_id = admin_data.get("id")


    # Fetch role data
    role_data = fetch_role(role_id)
    
    if not role_data:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # extract the role name from the role id
    role_name = role_data.get("name")


    # Verify password (given password with stored password)
    if not verify_password(password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")


    # Generate JWT token with user details
    access_token = create_token(data={"sub": email, "role": role_name, "id" : admin_id})


    return {"access_token": access_token, "token_type": "bearer"}


# Handles admin login and returns a JWT token.
def admin_login(email: str, password: str):
    
    return authenticate_admin(email, password)



"""
    Authenticates the user by verifying email and password.
    Fetches user details from UserService and generates JWT.

    Returns:
        dict: JWT access token if authentication is successful.
"""
def authenticate_user(email: str, password: str):

    user_data = fetch_user(email)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # extract the admin credentials required for authentication
    stored_password = user_data.get("password")
    role_id = user_data.get("role_id")
    user_id = user_data.get("user_id")
    user_status = user_data.get("status")

    if user_status != "ACTIVE":
        raise HTTPException(status_code=403, detail="You can access the Library only after approval. Thank You")

    role_data = fetch_user_role(role_id)

    if not role_data:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # extract the role name from the role id
    role_name = role_data.get("name")


    # Verify password (given password with stored password)
    if not verify_password(password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")


    # Generate JWT token with user details
    access_token = create_token(data={"sub": email, "role": role_name, "id" : user_id, "status": user_status})


    return {"access_token": access_token, "token_type": "bearer"}


# Handles user login and returns a JWT token.
def user_login(email: str, password: str):

    return authenticate_user(email, password)