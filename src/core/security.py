# core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.core.config import settings
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import Depends, HTTPException, status
from supabase import create_client
from supabase.lib.client_options import ClientOptions

# Security and authentication
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Initialize Supabase client
supabase_options = ClientOptions(
    schema='public',
    headers={'X-Client-Info': 'ai-school'},
    persist_session=True,
    auto_refresh_token=True,
)

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
    options=supabase_options
)

# Sign-up function
async def sign_up_user(email: str, password: str, username: str):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "data": {"username": username}
        })
        return response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# After the sign_up_user function
async def verify_email(token: str):
    try:
        response = supabase.auth.verify_otp({
            "token": token,
            "type": "email"
        })
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email verification failed: {str(e)}"
        )

# Sign-in function
async def sign_in_user(email: str, password: str):
    try:
        print(f"Attempting login with email: {email}")  # Debug log
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"Login response: {response}")  # Debug log
        
        if not response.user or not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return response
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}"
        )

# Fetch current user function
async def get_current_user(token: str):
    try:
        # Use Supabase's built-in token validation
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        print(f"Input password type: {type(plain_password)}")
        print(f"Hashed password type: {type(hashed_password)}")
        print(f"Input password length: {len(plain_password)}")
        print(f"Hashed password length: {len(hashed_password)}")
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"Verification result: {result}")
        return result
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        print(f"Error type: {type(e)}")
        return False

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    except JWTError as e:
        print(f"Token creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token"
        )
