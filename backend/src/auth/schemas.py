from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=8)
    full_name: str


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    full_name: str
    is_active: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
