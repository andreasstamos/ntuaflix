from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
from routes.admin import router as admin_router
from routes.index import router as index_router

env_path = '.env'
load_dotenv(dotenv_path=env_path)


def create_app():
    """
    Create a FastAPI application instance.
    """

    app = FastAPI()

    app.debug = bool(int(os.getenv('DEBUG')))
    
    app.include_router(index_router, prefix='ntuaflix_api/', tags=['index'])
    app.include_router(admin_router, prefix='ntuaflix_api/admin', tags=['admin'])

    return app

