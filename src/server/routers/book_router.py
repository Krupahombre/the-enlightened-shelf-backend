from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.book import BookResponse, BookPayload, BookSingleResponse
from src.service.book_service import get_books_list, add_book, get_book_single
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/books",
    tags=["Book"]
)


@router.get("/", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_books(db: db_dependency):
    return BookResponse(data=get_books_list(db))


@router.post("/", response_model=BookSingleResponse, status_code=status.HTTP_201_CREATED)
def create_book(token: token_dependency, db: db_dependency, payload: BookPayload):
    return BookSingleResponse(data=add_book(token, db, payload))


@router.get("/book/{book_id}", response_model=BookSingleResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(db: db_dependency, book_id: int = Path()):
    return BookSingleResponse(data=get_book_single(db, book_id))
