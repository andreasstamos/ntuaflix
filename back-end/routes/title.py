from fastapi import APIRouter, Depends
from models import Title
from sqlalchemy.orm import Session

from database import get_db

from pydantic import BaseModel, Field

class titleObject(BaseModel):
    tconst: str = Field(alias="titleID")

    class Config:
        from_attributes = True
        populate_by_name = True

router = APIRouter()

@router.get("/title/{titleID}", response_model=titleObject)
async def get_title(titleID: str, db:Session = Depends(get_db)):
    return db.query(Title).filter_by(tconst=titleID).first()

