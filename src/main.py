# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.session import AsyncSessionLocal
from api.v1.routes import user, rag, narration, auth
from sqlalchemy import text  # Add this import

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])  # Added auth router
    app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
    app.include_router(narration.router, prefix="/api/v1/narration", tags=["narration"])

    # Add root route
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to AI School API",
            "docs": "/docs",
            "status": "running"
        }

    return app

app = create_application()

@app.on_event("startup")
async def startup_event():
    try:
        # Check database connection
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))  # Modified this line
        
        # Validate required settings
        required_vars = ["GROQ_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
        missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Check Ollama connection
        try:
            import ollama
            ollama.embeddings(model="nomic-embed-text", prompt="test")
        except Exception as e:
            print(f"Warning: Ollama service not available: {e}")
        
        print(f"{settings.PROJECT_NAME} startup checks completed successfully!")
    except Exception as e:
        print(f"Startup check failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    # Add any cleanup logic
    print(f"{settings.PROJECT_NAME} is shutting down!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )