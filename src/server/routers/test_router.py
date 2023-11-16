from fastapi import APIRouter
from starlette import status

from src.database import User, Book
from src.database.database import db_dependency

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


@router.get("/test-user-reviews", status_code=status.HTTP_200_OK)
def test_user_reviews(db: db_dependency):
    user_id = 1
    user = db.query(User).filter(User.id == user_id).first()
    user_reviews = user.reviews
    return user_reviews


@router.get("/test-user-checkouts", status_code=status.HTTP_200_OK)
def test_user_checkouts(db: db_dependency):
    user_id = 1
    user = db.query(User).filter(User.id == user_id).first()
    user_checkouts = user.checkouts
    return user_checkouts


@router.get("/test-book-reviews", status_code=status.HTTP_200_OK)
def test_book_reviews(db: db_dependency):
    book_id = 3
    book = db.query(Book).filter(Book.id == book_id).first()
    book_reviews = book.reviews
    return book_reviews


@router.get("/test-book-checkouts", status_code=status.HTTP_200_OK)
def test_book_checkouts(db: db_dependency):
    book_id = 2
    book = db.query(Book).filter(Book.id == book_id).first()
    book_checkouts = book.checkouts
    return book_checkouts
