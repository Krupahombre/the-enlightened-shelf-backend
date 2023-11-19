from typing import Type

from sqlalchemy.orm import Session

from src.database.models.book import Book


def get_books(db: Session) -> list[Type[Book]] | None:
    return db.query(Book).order_by(Book.id).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def save_book(db: Session, book_model: Book) -> None:
    db.add(book_model)
    db.commit()


def remove_book(db: Session, book_model: Book) -> None:
    db.delete(book_model)
    db.commit()


def update_book(db: Session, book_model: Book) -> None:
    db.add(book_model)
    db.commit()
