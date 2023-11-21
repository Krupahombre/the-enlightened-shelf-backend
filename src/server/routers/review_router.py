from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.review import ReviewResponse, ReviewPayload
from src.service.review_service import get_reviews_for_book, create_review_for_book
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/reviews",
    tags=["Review"]
)


@router.get('/{book_id}', response_model=ReviewResponse, status_code=status.HTTP_200_OK)
def get_reviews_by_book_id(token: token_dependency, db: db_dependency, book_id: int = Path()):
    return ReviewResponse(data=get_reviews_for_book(token, db, book_id))


@router.post("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_review(token: token_dependency, db: db_dependency, payload: ReviewPayload, book_id: int = Path()):
    create_review_for_book(token, db, payload, book_id)
