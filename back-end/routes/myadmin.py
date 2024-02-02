from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from typing import Annotated, Optional
from sqlalchemy import text
import os

from utils import admin_required,role_dependency
from models import User
from schemas import UserObject, TitleObject
from utils import CSVResponse, FormatType

import pandas as pd

router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

def title_tsv_handler(tsv_file: str, db: db_dependency, success = [], fail=[]):
    df = pd.read_tsv(tsv_file, sep='\t')
    for idx, row in df.iterrows():
        title_data = {
            'tcnost': row['tconst'],
            'title_type': row['titleType'],
            'originalTitle': row['originalTitle'],
            'is_adult': (row['isAdult']=='1'),
            'start_year': int(row['startYear']) if row['startYear']!=r'\N' else None,
            'end_year': int(row['endYear']) if row['endYear']!=r'\N' else None,
            'runtime_minutes': int(row['runtimeMinutes']) if row['runtimeMinutes']!=r'\N' else None,
            'imgage_url': row['img_url_asset'] if row['img_url_asset']!=r'\N' else None,
            'genres': []
        }
        new_title = TitleObject(**title_data)
        try:
            db.add(new_title)
            db.commit()
            success.append(new_title)
        except Exception as e:
            fail.append(new_title)
    return success, fail
            
@router.post("/myadmin/upload/titlebasics")
async def upload_titles(
    role: role_dependency,
    db: db_dependency,
    titles_tsv: UploadFile):
    file_path = f"./tmp/{titles_tsv.filename}"
    with open(file_path, 'wb') as f:
        f.write(titles_tsv.file.read())    
    s,f = title_tsv_handler(file_path, db)   
    os.remove(file_path) 
    return s

""""
curl -X POST "http://127.0.0.1:8000/ntuaflix_api/myadmin/upload/titlebasics" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@/ntuaflix/softeng23-34/back-end/docs/truncated_title.basics.tsv"
"""

@router.get("/myadmin/healthcheck")
@admin_required
async def connection_status(role: role_dependency, db: db_dependency):
    response = {"status":"failed", "dataconnection": str(db.bind.url)}
    try:
        db.execute(text('SELECT 1'))
        response["status"] = "OK"
    except Exception as e:
        print(e)
    finally:
        return response
    
@router.post("/myadmin/usermod/{username}/{password}")
@admin_required
async def user_credentials(
    role: role_dependency, db: db_dependency, username: str, password: str):
    user = db.query(User).filter(User.username==username).first()
    if user:
        user.password = password #hash this
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"User {username} doesn't exist")

    
@router.get("/myadmin/users/{username}")
@admin_required
async def view_user_details(
    role: role_dependency, db: db_dependency, username:str,
    format: FormatType = FormatType.json):
    values = db.query(User).filter(User.username==username).all()
    if (values==[]):
        raise HTTPException(status_code=404, detail=f"User {username} doesn't exist!") 
    if format==FormatType.csv: pass
    return values

    