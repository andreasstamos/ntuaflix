from fastapi import APIRouter, Depends
from models import Title
from sqlalchemy.orm import Session
from database import get_db

from .title_schema import TitleObject, TqueryObject, GqueryObject

router = APIRouter()

@router.get("/title/{titleID}", response_model=TitleObject | None)
async def get_title(titleID: str, db: Session = Depends(get_db)):
    return db.query(Title).filter_by(tconst=titleID).first()

@router.get("/searchTitle")
@router.post("/searchTitle")
async def search_title_name(query: TqueryObject, db: Session = Depends(get_db)) -> list[TitleObject]:
    return db.query(Title).filter(Title.primary_title.contains(query.titlePart))

@router.get("/bygenre")
async def search_title_genre(query: GqueryObject, db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.genres.any(name=query.qgenre)).filter(Title.average_rating >= query.minrating)
    if query.yrFrom is not None and query.yrTo is not None:
        titles = titles.filter(query.yrFrom <= Title.start_year).filter(Title.start_year <= query.yrTo)
    return titles

