from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Person
from schemas import NameObject, NqueryObject

router = APIRouter()

@router.get("/name/{nameID}", response_model = Optional[NameObject])
async def get_person(nameID: str, db: Session = Depends(get_db)):
    return db.query(Person).filter_by(nconst=nameID).first()

@router.get("/searchname")
@router.post("/searchname")
async def search_person_name(query: NqueryObject, db: Session = Depends(get_db)) -> list[NameObject]:
    return db.query(Person).filter(Person.primary_name.contains(query.namePart))

