from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreate, UserLogin, UserResponse, Token
from .service import auth_service
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user with email and password
    """
    return await auth_service.register(user_data)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password
    """
    return await auth_service.login(credentials)


@router.post("/logout")
async def logout(current_user: UserResponse = Depends(get_current_user)):
    """
    Logout the current user
    """
    success = await auth_service.logout(current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not logout user"
        )
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user
