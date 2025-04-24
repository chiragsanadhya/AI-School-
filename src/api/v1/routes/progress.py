from fastapi import APIRouter, HTTPException, Depends
from src.core.auth import get_current_user
from src.services.content_service import ContentService

router = APIRouter()
content_service = ContentService()

@router.get("/")
async def get_progress(current_user = Depends(get_current_user)):
    try:
        return {"message": "Progress tracking coming soon"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/streak")
async def update_streak(current_user = Depends(get_current_user)):
    try:
        return {"message": "Streak update coming soon"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tests")
async def get_test_results(current_user = Depends(get_current_user)):
    try:
        return {"message": "Test results coming soon"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))