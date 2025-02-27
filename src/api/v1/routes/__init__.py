from fastapi import APIRouter
from .narration import router as narration_router
from .rag import router as rag_router
from .test import router as test_router
from .user import router as user_router

# Initialize main router
router = APIRouter()

# Include different module routers
router.include_router(narration_router, prefix="/narration", tags=["Narration"])
router.include_router(rag_router, prefix="/rag", tags=["RAG"])
router.include_router(test_router, prefix="/test", tags=["Test"])
router.include_router(user_router, prefix="/user", tags=["User"])
