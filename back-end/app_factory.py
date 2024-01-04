from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
from routes.admin import router as admin_router
from routes.index import router as index_router
from routes.auth import router as auth_router
from routes.title import router as title_router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base
from database import engine, get_db
import logging
env_path = '.env'
load_dotenv(dotenv_path=env_path)



def create_app():
    """
    Create a FastAPI application instance.
    """

    app = FastAPI()
    # if bool(int(os.getenv('DEBUG'))):
        # logging.basicConfig(level=logging.DEBUG)
    # Database engine
    # Create tables on startup
    Base.metadata.create_all(bind=engine)

    app.debug = bool(int(os.getenv('DEBUG')))
    
    app.include_router(index_router, prefix='/ntuaflix_api', tags=['index'])
    app.include_router(auth_router, prefix='/ntuaflix_api', tags=['auth'])
    app.include_router(admin_router, prefix='/ntuaflix_api/admin', tags=['admin'])

    app.include_router(title_router, prefix='/ntuaflix_api', tags=['title'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return app
