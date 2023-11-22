import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database import Checkout
from src.database.dals.book_dal import get_book, update_book
from src.database.dals.checkout_dal import get_checkouts_admin, save_checkout, get_checkouts_by_user_id
from src.database.dals.user_dal import get_user_by_id
from src.server.models.checkout import CheckoutAdminDTO, CheckoutDTO
from src.service.auth_service import check_admin_role
from src.utils.email_sender.sender import email_sender
from src.utils.qr_utils import create_qr_data, create_qr_code_dto

logger = logging.getLogger("CheckoutService")


def get_checkouts_list_admin(token: dict, db: Session) -> Optional[List[CheckoutAdminDTO]]:
    logger.info("Fetch secured checkouts request occurred")
    if not check_admin_role(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorize to do this action!"
        )

    try:
        checkouts = get_checkouts_admin(db)

        if not checkouts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no checkouts to display"
            )

        checkout_list = []
        for checkout in checkouts:
            book_name = checkout.book.title if checkout.book else None

            qr_code = create_qr_code_dto(checkout.id, checkout.qr_code_data)

            checkout_dto = CheckoutAdminDTO(
                id=checkout.id,
                user_email=checkout.user.email,
                book_name=book_name,
                checkout_date=checkout.checkout_date,
                return_date=checkout.return_date,
                qr_code_data=qr_code
            )
            checkout_list.append(checkout_dto)

        return checkout_list
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def get_checkouts_list(token: dict, db: Session) -> Optional[List[CheckoutDTO]]:
    logger.info("Fetch checkouts request occurred")
    try:
        user = get_user_by_id(db, token["id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )

        checkouts = get_checkouts_by_user_id(db, user.id)
        if not checkouts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no checkouts to display"
            )

        checkout_list = []
        for checkout in checkouts:
            book_name = checkout.book.title if checkout.book else None

            checkout_dto = CheckoutDTO(
                id=checkout.id,
                book_name=book_name,
                checkout_date=checkout.checkout_date,
                return_date=checkout.return_date
            )
            checkout_list.append(checkout_dto)

        return checkout_list
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def create_checkout(token: dict, db: Session, book_id: int) -> None:
    logger.info("Create checkout occurred")
    try:
        book = get_book(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found!"
            )
        user = get_user_by_id(db, token["id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )

        user_checkouts = user.checkouts

        for checkout in user_checkouts:
            if checkout.book_id == book_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot checkout the same book twice!"
                )

        checkout_date = datetime.now()
        return_date = checkout_date + timedelta(days=7)

        checkout_model = Checkout()

        checkout_model.user_id = user.id
        checkout_model.book_id = book_id
        checkout_model.checkout_date = checkout_date.strftime("%Y-%m-%d %H:%M:%S")
        checkout_model.return_date = return_date.strftime("%Y-%m-%d %H:%M:%S")
        checkout_model.qr_code_data = create_qr_data(user, book, checkout_date.strftime("%Y-%m-%d %H:%M:%S"))

        db_checkout = save_checkout(db, checkout_model)

        book.quantity_available -= 1
        update_book(db, book)

        qr_data = create_qr_code_dto(db_checkout.id, db_checkout.qr_code_data)
        email_sender.send_email(user.email, qr_data)
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise
