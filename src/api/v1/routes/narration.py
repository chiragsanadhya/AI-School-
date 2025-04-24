from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.ml.narration import TextProcessor, Narrator
from src.core.security import security, get_current_user
import os
from src.services.narration_service import NarrationService

router = APIRouter()
narration_service = NarrationService()

# Get API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key is available
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize the processors
text_processor = TextProcessor(api_key=GROQ_API_KEY)
narrator = Narrator()

@router.get("/")
async def get_narrations(credentials: HTTPAuthorizationCredentials = Depends(security)):
    await get_current_user(credentials.credentials)
    return {"message": "Narration endpoint"}

@router.post("/narrate")
async def narrate(
    text: str, 
    background_tasks: BackgroundTasks, 
    transform: bool = False,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    await get_current_user(credentials.credentials)
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    processed_text = text_processor.transform(text) if transform else text
    background_tasks.add_task(narrator.narrate, processed_text)
    return {"message": "Narration queued successfully"}

@router.post("/")
async def narrate_text(text: str):
    try:
        result = narration_service.narrate(text)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
