from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.book import BookResponse, BookPayload, BookSingleResponse, BookUpdatePayload
from src.service.book_service import get_books_list, add_book, get_book_single, delete_book, change_book
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/books",
    tags=["Book"]
)


@router.get("/", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_books(db: db_dependency):
    return BookResponse(data=get_books_list(db))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(token: token_dependency, db: db_dependency, payload: BookPayload):
    add_book(token, db, payload)


@router.get("/book/{book_id}", response_model=BookSingleResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(db: db_dependency, book_id: int = Path()):
    return BookSingleResponse(data=get_book_single(db, book_id))


@router.put("/book/{book_id}", status_code=status.HTTP_202_ACCEPTED)
def manage_book_quantity(token: token_dependency, db: db_dependency, book_payload: BookUpdatePayload, book_id: int = Path()):
    change_book(token, db, book_id, book_payload)


@router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(token: token_dependency, db: db_dependency, book_id: int = Path()):
    delete_book(token, db, book_id)
