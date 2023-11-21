import logging
from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database import Review
from src.database.dals.book_dal import get_book
from src.database.dals.review_dal import get_reviews_by_book_id, save_review
from src.database.dals.user_dal import get_user_by_id
from src.server.models.review import ReviewDTO, ReviewPayload

logger = logging.getLogger("ReviewService")


def get_reviews_for_book(token: dict, db: Session, book_id: int) -> Optional[List[ReviewDTO]]:
    token_user = get_user_by_id(db, token["id"])
    if not token_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )
    try:
        reviews = get_reviews_by_book_id(db, book_id)
        reviews_response = []

        for review in reviews:
            username = review.user.username

            review_dto = ReviewDTO(
                id=review.id,
                username=username,
                date=review.date,
                rating=review.rating,
                comment=review.comment
            )
            reviews_response.append(review_dto)

        return reviews_response
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def create_review_for_book(token: dict, db: Session, payload: ReviewPayload, book_id: int) -> None:
    user = get_user_by_id(db, token["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    book = get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found!"
        )
    try:
        review_model = Review()

        review_model.user_id = user.id
        review_model.book_id = book_id
        review_model.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        review_model.rating = payload.rating
        review_model.comment = payload.comment

        save_review(db, review_model)
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise

