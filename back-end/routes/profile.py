from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, Delete, Update, exc
from sqlalchemy.orm import Session
from database import get_db
from datetime import date
from pydantic import BaseModel
from utils import CSVResponse, FormatType
from fastapi.responses import JSONResponse

from models import User
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import authorize_user, token_dependency

router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/user-profile/{user_id}")
@authorize_user
async def profile(
    user_id: int,
    session_id: token_dependency,
    db: db_dependency,
    format: FormatType = FormatType.json):
    """"Get user profile"""
    user_profile = db.query(User).filter(User.id == user_id).first()
    print(f'User profile: {user_profile}')
    if user_profile==None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    else:
        return user_profile

@router.get("/update-profile/{user_id}")
@authorize_user
async def update_profile(
    user_id: int,
    session_id: token_dependency,
    db: db_dependency,
    payload,
    format: FormatType = FormatType.json):
    """"Update user profile"""
    user_profile = db.query(User).filter(User.id == user_id).first()
    print(f'User profile: {user_profile}')
    if user_profile==None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    else:
        user_profile.first_name = user_profile.get("first_name", user_profile.first_name)
        user_profile.last_name = user_profile.get("last_name", user_profile.last_name)

        db.add(user_profile)
        db.commit()