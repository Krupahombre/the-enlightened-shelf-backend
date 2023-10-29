from typing import Type

from sqlalchemy.orm import Session

from src.database.models.book import Book


def get_books(db: Session) -> list[Type[Book]] | None:
    return db.query(Book).all()


def save_book(db: Session, book_model: Book) -> Book | None:
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model
