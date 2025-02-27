from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user_schema import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their email."""
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    """Retrieve all users from the database."""
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update user details."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user from the database."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
