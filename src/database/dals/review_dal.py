from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.database import Review


def get_reviews_by_book_id(db: Session, book_id: int) -> list[Type[Review]] | None:
    return db.query(Review).filter(Review.book_id == book_id).order_by(desc(Review.date)).all()


def save_review(db: Session, review_model: Review) -> None:
    db.add(review_model)
    db.commit()
