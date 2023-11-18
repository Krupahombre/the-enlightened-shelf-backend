import base64
import logging
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from src.database.dals.checkout import get_checkouts_admin
from src.server.models.checkout import CheckoutAdminDTO
from src.service.auth_service import check_admin_role

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

            checkout_dto = CheckoutAdminDTO(
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
