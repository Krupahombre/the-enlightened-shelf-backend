import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.dals.user_dal import get_user_by_id, get_user_by_username
from src.server.models.auth import LoginPayload
from src.server.models.user import UserDTO
from src.utils.password_utils import verify_password

logger = logging.getLogger("UserService")


def authenticate_user(db: Session, payload: LoginPayload):
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
