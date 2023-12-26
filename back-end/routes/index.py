from fastapi import APIRouter

router = APIRouter()

# Index Route File

@router.get('/')
async def index():
    return {"message": "Hello World from index!"}