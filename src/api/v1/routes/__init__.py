from fastapi import APIRouter
from .auth import router as auth_router
from .chapters import router as chapters_router
from .progress import router as progress_router
from .ml import router as ml_router
from .narration import router as narration_router
from .rag import router as rag_router
from .test import router as test_router
from .user import router as user_router
# Comment out or fix the narration import
# from .narration import router as narration_router

# Initialize main router
router = APIRouter()

# Include routers
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(chapters_router, prefix="/chapters", tags=["Chapters"])

# Include different module routers
# Fix: Add error handling for router initialization
try:
    router.include_router(narration_router, prefix="/narration", tags=["Narration"])
    router.include_router(rag_router, prefix="/rag", tags=["RAG"])
    router.include_router(test_router, prefix="/test", tags=["Test"])
    router.include_router(user_router, prefix="/users", tags=["users"])
except Exception as e:
    print(f"Error initializing routes: {e}")
    raise
