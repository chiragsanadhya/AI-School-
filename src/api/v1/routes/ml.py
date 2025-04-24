from fastapi import APIRouter, HTTPException
from src.services.ml_service import MLService

router = APIRouter()
ml_service = MLService()

@router.post("/explain")
async def get_explanation(text: str):
    try:
        explanation = ml_service.get_explanation(text)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/narrate")
async def generate_narration(text: str):
    try:
        result = ml_service.generate_narration(text)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_context(message: str):
    try:
        response = ml_service.chat_with_context(message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))