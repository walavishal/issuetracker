from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, name: str, password: str):
    user = User(
        email=email,
        name=name,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



def update_user_profile(db: Session, user: User, name: str):
    user.name = name
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user: User, current_password: str, new_password: str):
    # verify current password
    if not verify_password(current_password, user.hashed_password):
        return False

    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return True

def get_user_or_404(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user