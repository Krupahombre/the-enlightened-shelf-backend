import logging
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.dals.user_dal import get_user_by_id, get_user_by_username, get_user_by_email, save_user
from src.database.models.user import User
from src.server.models.auth import LoginPayload, RegisterPayload
from src.server.models.user import UserDTO
from src.utils.password_utils import verify_password, get_hashed_password

logger = logging.getLogger("UserService")


def login_authentication(db: Session, payload: LoginPayload) -> Optional[UserDTO]:
    try:
        username = payload.username
        password = payload.password

        user = get_user_by_username(db, username)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def validate_user(db: Session, payload: RegisterPayload) -> bool:
    try:
        username = payload.username
        email = payload.username

        username_validator = get_user_by_username(db, username)
        email_validator = get_user_by_email(db, email)

        if username_validator is not None or email_validator is not None:
            return False
        else:
            return True

    except HTTPException as e:
        logger.error(e)
        raise
    except Exception as e:
        logger.error(e)
        raise


def create_user(db: Session, payload: RegisterPayload) -> Optional[UserDTO]:
    try:
        user_model = User()

        user_model.email = payload.email
        user_model.username = payload.username
        user_model.first_name = payload.first_name
        user_model.last_name = payload.last_name
        user_model.password = get_hashed_password(payload.password)

        return save_user(db, user_model)
    except HTTPException as e:
        logger.error(e)
        raise
    except Exception as e:
        logger.error(e)
        raise


def get_user(db: Session, user_id: int) -> UserDTO:
    try:
        user = get_user_by_id(db, user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise
