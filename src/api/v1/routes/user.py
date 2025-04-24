from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from src.schemas.user_schema import UserCreate, UserLogin
from src.core.security import (
    sign_up_user, 
    sign_in_user, 
    get_current_user, 
    security,
    verify_email
)

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    try:
        user_data = await sign_up_user(user.email, user.password, user.username)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Registration successful. Please check your email for verification.",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(user_credentials: UserLogin):
    try:
        auth_response = await sign_in_user(user_credentials.email, user_credentials.password)
        # Include default stats in the response
        user_dict = {
            "id": auth_response.user.id,
            "email": auth_response.user.email,
            "username": auth_response.user.email.split('@')[0],
            "stats": {
                "chaptersCompleted": 0,
                "testsTaken": 0,
                "averageScore": 0,
                "rank": 0,
                "totalUsers": 0,
                "streak": 0,
                "lastActive": "Just joined"
            },
            "recentCourses": [],
            "achievements": []
        }
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": auth_response.session.access_token,
                "token_type": "bearer",
                "user": user_dict
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.get("/me")
async def get_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = await get_current_user(credentials.credentials)
        # Convert user data to dictionary
        user_dict = {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/verify-email/{token}")
async def verify_email(token: str):
    try:
        response = await verify_email(token)
        return {"message": "Email verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))