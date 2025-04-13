from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

ALGORITHM = os.getenv("ALGORITHM")


# generate JWT
def create_token(data: dict, expire_date: timedelta = None):

    data_encode = data.copy()

    expire = datetime.now() + (expire_date or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))

    return jwt.encode(data_encode, SECRET_KEY, algorithm=ALGORITHM)


# verify JWT
def verify_token(token: str):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload       # returns decoded user data
    
    except:
        return None

    