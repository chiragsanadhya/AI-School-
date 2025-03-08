from fastapi import APIRouter, HTTPException
from ml.narration import TextProcessor, Narrator
import os

router = APIRouter()

# Initialize classes
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

text_processor = TextProcessor(api_key=GROQ_API_KEY)
narrator = Narrator()

# Fix: Add background tasks for audio processing
from fastapi import BackgroundTasks

@router.post("/narrate/")
async def narrate(text: str, background_tasks: BackgroundTasks, transform: bool = False):
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    processed_text = text_processor.transform(text) if transform else text
    background_tasks.add_task(narrator.narrate, processed_text)
    return {"message": "Narration queued successfully"}
