from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text, MetaData
import codecs

from models import *
from database import get_db
from utils import FormatType, CSVResponse
from utils import parse_title_basics, parse_title_ratings, parse_title_principals,\
        parse_title_crew, parse_title_akas, parse_name_basics, parse_title_episode
from schemas import HealthCheckObject, ResetAllObject, UploadFileObject

router = APIRouter()

@router.get('/healthcheck')
async def health_check(
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> HealthCheckObject:
    """Returns health status of backend and database."""
    ret = {"status": "failed", "dataconnection": str(db.bind.url)}
    try:
        if db.execute(text('SELECT 1')).first() == (1,):
            ret = {"status": "OK", "dataconnection": str(db.bind.url)}
    except:
        pass
    if format == FormatType.csv: return CSVResponse([HealthCheckObject.model_validate(ret)])
    return ret

@router.post('/resetall')
async def reset_all(
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> ResetAllObject:
    """Resets database to initial state."""
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    #TODO: what about failure? why would it fail in a manner that is not a bug, so that we would want the user to know?
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([ResetAllObject.model_validate(ret)])
    return ret

class UploadFileAdapter:
    def __init__(self, file):
        self.file = file
        self.decoder = codecs.getincrementaldecoder("utf-8")()

    async def read(self, n):
        data = await self.file.read(max(4,n))
        data = self.decoder.decode(data)
        return data

@router.post('/upload/titlebasics')
async def upload_title_basics(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Title Basics."""
    if db.query(db.query(Title).exists()).scalar():
        ret = {"status": "failed", "reason": "Titles table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_basics(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleakas')
async def upload_title_akas(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Title Aliases."""
    if db.query(db.query(TitleAlias).exists()).scalar():
        ret = {"status": "failed", "reason": "Titles Alias table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_akas(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/namebasics')
async def upload_name_basics(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Name Basics."""
    if db.query(db.query(Person).exists()).scalar():
        ret = {"status": "failed", "reason": "Person table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_name_basics(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titlecrew')
async def upload_title_crew(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Crew Basics."""
    if db.query(db.query(Title).join(Title.directors).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Directors table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    if db.query(db.query(Title).join(Title.writers).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Writers table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_crew(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleepisode')
async def upload_title_episode(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Title Episode."""
    if db.query(db.query(TitleEpisode).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Episodes table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_episode(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret


@router.post('/upload/titleprincipals')
async def upload_title_principals(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Title Principals."""
    if db.query(db.query(Principals).exists()).scalar():
        ret = {"status": "failed", "reason": "Principals table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_principals(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleratings')
async def upload_title_ratings(
        file: UploadFile,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> UploadFileObject:
    """Upload .tsv file for Title Ratings."""
    await parse_title_ratings(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

