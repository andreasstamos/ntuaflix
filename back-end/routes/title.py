from fastapi import APIRouter, Depends
from models import Title
from sqlalchemy.orm import Session
from database import get_db

from .title_schema import TitleObject

router = APIRouter()

@router.get("/title/{titleID}", response_model=TitleObject)
async def get_title(titleID: str, db:Session = Depends(get_db)):
    return db.query(Title).filter_by(tconst=titleID).first()

