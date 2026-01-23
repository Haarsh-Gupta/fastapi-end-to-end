from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
from ..schema.user_schema import UserPayload
from ..models.user_model import User
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_here") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id") 

        if user_id is None:
            raise credentials_exception
        
        token_data = UserPayload(**payload)
        
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    data = verify_access_token(token, credentials_exception)
    return data
