from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Title
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import CSVResponse, FormatType

router = APIRouter()

@router.get("/title/{titleID}", response_model = Optional[TitleObject])
async def get_title(
        titleID: str,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ):
    title = db.query(Title).filter_by(tconst=titleID).first()
    if format == FormatType.csv: return CSVResponse([TitleObject.model_validate(title)] if title is not None else [])
    return title

@router.get("/searchtitle")
@router.post("/searchtitle")
async def search_title_name(
        query: TqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.primary_title.contains(query.titlePart))
    if format == FormatType.csv: return CSVResponse(map(TitleObject.model_validate, titles))
    return titles

@router.get("/bygenre")
async def search_title_genre(
        query: GqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.genres.any(name=query.qgenre)).filter(Title.average_rating >= query.minrating)
    if query.yrFrom is not None and query.yrTo is not None:
        titles = titles.filter(query.yrFrom <= Title.start_year).filter(Title.start_year <= query.yrTo)
    if format == FormatType.csv: return CSVResponse(map(TitleObject.model_validate, titles))
    return titles

TITLES_PER_PAGE = 28

@router.get("/get-movies")
async def get_movies(page:int or None = 1, qgenre: int or None = None, db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).limit(TITLES_PER_PAGE)
    if qgenre:
        titles = titles.filter(Title.genres.any(id=qgenre))
    return titles
