import logging
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.dals.book_dal import get_books, save_book, get_book
from src.database.models.book import Book
from src.server.models.book import BookDTO, BookPayload
from src.service.auth_service import check_admin_role

logger = logging.getLogger("BookService")


def get_books_list(db: Session) -> Optional[List[BookDTO]]:
    logger.info("Fetch books request occurred")
    try:
        books = get_books(db)

        return books
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def get_book_single(db: Session, book_id: int) -> Optional[BookDTO]:
    logger.info("Fetch book request occurred")
    try:
        books = get_book(db, book_id)

        return books
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise

def add_book(token: dict, db: Session, payload: BookPayload) -> Optional[BookDTO]:
    logger.info("Add book request occurred")
    if not check_admin_role(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorize to do this action!"
        )

    try:
        book_model = Book()

        book_model.title = payload.title
        book_model.author = payload.author
        book_model.description = payload.description
        book_model.quantity = payload.quantity
        book_model.quantity_available = payload.quantity
        book_model.category = payload.category
        book_model.img = payload.img

        return save_book(db, book_model)
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise
