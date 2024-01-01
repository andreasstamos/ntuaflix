from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import  Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, constr
from models import User
from database import get_db
from datetime import date
from sqlalchemy import exc

# Authentication Router

router = APIRouter()

SECRET_KEY = "469155679be5db1afdb6613292c4c7805dfa71d2be7fde22d5abb522d6f23ef2"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password):
    return pwd_context.hash(password)

class UserLoginRequirements(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(payload: UserLoginRequirements, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if user and verify_password(payload.password, user.password):
        token_data = {
            'username': user.username,
            'role': 'admin' if user.is_admin else 'user',
            'user_id': user.id,
        }
        token = create_jwt_token(token_data)
        return {'token': token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
class UserRegisterRequirements(BaseModel):
    username: constr(min_length=4)
    first_name: constr(min_length=4)
    last_name: constr(min_length=4)
    email: EmailStr
    dob: date
    password: constr(min_length=4)
    password_confirm: constr(min_length=4)

    class Config:
        json_schema_extra = {
            "payload": {
                "username": "Konstantinos Pikoulas",
                "first_name": "Konstantinos",
                "last_name": "Pikoulas",
                "email": "kostas.pik@example.com",
                "dob": "2002-01-01",
                "password": "secretpassword",
                "password_confirm": "secretpassword",
            }
        }

@router.post('/register')
async def register(payload: UserRegisterRequirements = Body(..., embed=True), db:Session = Depends(get_db)):
    if (payload.password != payload.password_confirm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match.",
        )
    try:
        payload.password = get_password_hash(payload.password)
        new_user = User(**payload.model_dump(mode='json', exclude=['password_confirm']))
        db.add(new_user)
        db.commit()
        db.refresh
        return JSONResponse(content={"message": "This is where you register!"}, status_code=200)
    
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to register account. Username or Email are probably being already used.'
        )
