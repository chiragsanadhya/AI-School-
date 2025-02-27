from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """Base schema for user details."""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user details."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """Schema for returning user details (without password)."""
    id: int

    class Config:
        from_attributes = True
