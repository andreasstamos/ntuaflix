from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from functools import wraps
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user_id

token_dependency = Annotated[int ,Depends(get_current_user)]

def authorize_user(func):
    @wraps(func)
    async def wrapper(*args, user_id: int, session_id: token_dependency, **kwargs):
        if user_id != session_id:
            raise HTTPException(status_code=403, detail="Permission denied: Cross user validation failed")
        return await func(*args, user_id=user_id, session_id=session_id, **kwargs)
    return wrapper