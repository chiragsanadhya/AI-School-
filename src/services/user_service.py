from sqlalchemy.orm import Session
from src.db.queries import create_user, get_user_by_email
from src.core.security import hash_password, verify_password
from src.schemas.user_schema import UserCreate
from src.models.user import User

# ✅ 1. Register a new user (with password hashing)
def register_user(db: Session, user_data: UserCreate):
    hashed_pw = hash_password(user_data.password)
    return create_user(db, username=user_data.username, email=user_data.email, hashed_password=hashed_pw)

# ✅ 2. Authenticate user (verify password)
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None  # Authentication failed
    return user  # Authentication successful
