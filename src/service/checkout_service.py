import base64
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from src.database import Checkout
from src.database.dals.book_dal import get_book
from src.database.dals.checkout_dal import get_checkouts_admin, save_checkout
from src.database.dals.user_dal import get_user_by_id
from src.server.models.checkout import CheckoutAdminDTO, CheckoutAdminDTOImage
from src.service.auth_service import check_admin_role
from src.utils.qr_utils import create_qr_data

logger = logging.getLogger("CheckoutService")


def get_checkouts_list_admin(token: dict, db: Session) -> Optional[List[CheckoutAdminDTO]]:
    logger.info("Fetch checkouts request occurred")
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
            user_first_name = checkout.user.first_name if checkout.user else None
            user_last_name = checkout.user.last_name if checkout.user else None
            user_full_name = user_first_name + " " + user_last_name
            book_name = checkout.book.title if checkout.book else None

            checkout_dto = CheckoutAdminDTO(
                id=checkout.id,
                user_full_name=user_full_name,
                book_name=book_name,
                checkout_date=checkout.checkout_date,
                return_date=checkout.return_date,
                qr_code_data=checkout.qr_code_data
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

        user_checkouts = user.checkouts

        for checkout in user_checkouts:
            if checkout.book_id == book_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot check out the same book twice!"
                )

        checkout_date = datetime.now()
        return_date = checkout_date + timedelta(days=7)

        checkout_model = Checkout()

        checkout_model.user_id = user.id
        checkout_model.book_id = book_id
        checkout_model.checkout_date = checkout_date.strftime("%Y-%m-%d %H:%M:%S")
        checkout_model.return_date = return_date.strftime("%Y-%m-%d %H:%M:%S")
        checkout_model.qr_code_data = create_qr_data(user, book, checkout_date.strftime("%Y-%m-%d %H:%M:%S"))

        save_checkout(db, checkout_model)
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def get_file(token: dict, db: Session):
    logger.info("Fetch checkouts request occurred")
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
        default_user_image_path = Path("src/images/default-user.jpg")
        checkout_list = []
        for checkout in checkouts:
            user_first_name = checkout.user.first_name if checkout.user else None
            user_last_name = checkout.user.last_name if checkout.user else None
            user_full_name = user_first_name + " " + user_last_name
            book_name = checkout.book.title if checkout.book else None

            with open(default_user_image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            checkout_dto = CheckoutAdminDTOImage(
                id=checkout.id,
                user_full_name=user_full_name,
                book_name=book_name,
                checkout_date=checkout.checkout_date,
                return_date=checkout.return_date,
                qr_code=encoded_image
            )
            checkout_list.append(checkout_dto)

        return checkout_list
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise
