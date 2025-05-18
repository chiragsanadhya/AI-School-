from supabase import create_client, Client
from fastapi import HTTPException, status
from .config import get_settings
from .schemas import UserCreate, UserLogin, UserResponse, Token
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        settings = get_settings()
        logger.info(f"Initializing Supabase client with URL: {settings.SUPABASE_URL}")
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    async def register(self, user_data: UserCreate) -> UserResponse:
        try:
            logger.info(f"Attempting to register user with email: {user_data.email}")
            logger.info(f"Using Supabase URL: {self.supabase.supabase_url}")
            logger.info(f"API Key length: {len(self.supabase.supabase_key) if self.supabase.supabase_key else 0}")
            
            # Create user in Supabase with email verification disabled
            try:
                response = self.supabase.auth.sign_up({
                    "email": user_data.email,
                    "password": user_data.password,
                    "options": {
                        "data": {
                            "full_name": user_data.full_name
                        },
                        "email_confirm": False  # Disable email verification
                    }
                })
                logger.info(f"Supabase response: {response}")
            except Exception as supabase_error:
                logger.error(f"Supabase error details: {str(supabase_error)}")
                logger.error(f"Error type: {type(supabase_error)}")
                raise
            
            if not response.user:
                logger.error("No user in response")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not create user"
                )
            
            return UserResponse(
                id=response.user.id,
                email=response.user.email,
                full_name=user_data.full_name
            )
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def login(self, credentials: UserLogin) -> Token:
        try:
            # Sign in with Supabase
            response = self.supabase.auth.sign_in_with_password({
                "email": credentials.email,
                "password": credentials.password
            })
            
            if not response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            return Token(
                access_token=response.session.access_token
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        try:
            # Get user from Supabase using the token
            user = self.supabase.auth.get_user(token)
            
            if not user:
                return None
                
            return UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.user_metadata.get("full_name", "")
            )
            
        except Exception:
            return None

    async def logout(self, token: str) -> bool:
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception:
            return False


auth_service = AuthService()
