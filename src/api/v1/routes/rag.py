from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.ml.rag import RAGChatbot

# Initialize FastAPI router
router = APIRouter()

# Load RAG chatbot instance
chatbot = RAGChatbot()

# Request model
class QueryRequest(BaseModel):
    question: str

@router.post("/chat")
def chat_with_rag(query: QueryRequest):
    """Handle user queries and return responses from the RAG chatbot."""
    try:
        response = chatbot.chat(query.question)
        return {"question": query.question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
