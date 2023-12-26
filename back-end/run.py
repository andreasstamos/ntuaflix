from app_factory import create_app
import uvicorn
from dotenv import load_dotenv
import os

env_path = '.env'
load_dotenv(dotenv_path=env_path)


if __name__ == '__main__':

    app = create_app()

    uvicorn.run(app, host=str(os.getenv('HOST')), port=int(os.getenv('PORT')))