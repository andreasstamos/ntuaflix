from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Person
from schemas import NameObject, NqueryObject
from utils import CSVResponse, FormatType

router = APIRouter()

@router.get("/name/{nameID}", response_model = Optional[NameObject])
async def get_person(
        nameID: str,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)):
    person = db.query(Person).filter_by(nconst=nameID).first()
    if format == FormatType.csv: return CSVResponse([NameObject.model_validate(person)] if person is not None else [])
    return person

@router.get("/searchname")
@router.post("/searchname")
async def search_person_name(
        query: NqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[NameObject]:
    people = db.query(Person).filter(Person.primary_name.contains(query.namePart))
    if format == FormatType.csv: return CSVResponse(map(NameObject.model_validate, people))
    return people

