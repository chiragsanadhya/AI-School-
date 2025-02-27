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

@router.post("/narrate/")
async def narrate(text: str, transform: bool = False):
    """
    Endpoint to generate narration.
    - If `transform=True`, it will first process the text using Groq's LLM.
    - Otherwise, it will directly generate the narration.
    - The generated speech will play in real-time.
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Apply transformation if required
    processed_text = text_processor.transform(text) if transform else text

    # Play narration
    narrator.narrate(processed_text)

    return {"message": "Narration played successfully"}
