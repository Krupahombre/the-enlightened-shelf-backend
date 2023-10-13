from typing import Optional

from sqlalchemy.orm import Session

from src.database.models.user import User


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, user_username: str) -> Optional[User]:
    return db.query(User).filter(User.username == user_username).first()


def get_user_by_email(db: Session, user_email: str) -> Optional[User]:
    return db.query(User).filter(User.email == user_email).first()


def save_user(db: Session, user_model: User) -> Optional[User]:
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model
