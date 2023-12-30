from fastapi import APIRouter

router = APIRouter()

# Admin Route File

@router.get('/')
async def admin():
    return {"message": "Hello World from admin!"}