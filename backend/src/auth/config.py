from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    # JWT settings
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    logger.info("Loaded settings:")
    logger.info(f"SUPABASE_URL: {settings.SUPABASE_URL}")
    logger.info(f"SUPABASE_KEY length: {len(settings.SUPABASE_KEY) if settings.SUPABASE_KEY else 0}")
    logger.info(f"SUPABASE_JWT_SECRET length: {len(settings.SUPABASE_JWT_SECRET) if settings.SUPABASE_JWT_SECRET else 0}")
    return settings
