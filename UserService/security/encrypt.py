from passlib.context import CryptContext


# Create a password hashing context with Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


"""Hashes a plain text password using Argon2."""
def hash_password(plain_password: str) -> str:
    
    return pwd_context.hash(plain_password)


"""Verifies if the given plain password matches the hashed password."""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    return pwd_context.verify(plain_password, hashed_password)
