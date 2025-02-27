import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the application."""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    class Config:
        env_file = ".env"  # Load settings from .env file
        extra = "allow"  # Allow additional environment variables

# Global settings instance
settings = Settings()
