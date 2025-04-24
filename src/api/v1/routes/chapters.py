from fastapi import APIRouter, HTTPException
from src.services.content_service import ContentService

router = APIRouter()
content_service = ContentService()

@router.get("/")
async def get_chapters():
    try:
        chapters = await content_service.get_chapters()
        return chapters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chapter_id}")
async def get_chapter_content(chapter_id: str):
    try:
        content = await content_service.get_chapter_content(chapter_id)
        if not content:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return content
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))