from sqlalchemy.orm import Session

from src.database.models.user import User


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, user_username: str):
    return db.query(User).filter(User.username == user_username).first()
