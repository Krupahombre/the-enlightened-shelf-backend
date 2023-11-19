import logging
from fastapi import HTTPException

from sqlalchemy.orm import Session
from starlette import status

from src.server.models.auth import LoginPayload, AuthDTO, RegisterPayload
from src.service.user_service import login_authentication, validate_user, create_user
from src.utils.token_utils import create_token

logger = logging.getLogger("AuthService")


def login_user(db: Session, payload: LoginPayload) -> AuthDTO:
    try:
        user = login_authentication(db, payload)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Couldn't find user with provided credentials."
            )

        token = create_token(user.id, user.username, user.role)

        auth_data = AuthDTO(
            username=user.username,
            role=user.role,
            token=token
        )

        return auth_data
    except HTTPException as e:
        logger.exception(e)
        raise
    except Exception as e:
        logger.exception(e)
        raise


def register_user(db: Session, payload: RegisterPayload) -> AuthDTO:
    try:
        validation = validate_user(db, payload)

        if not validation:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with provided data already exists!"
            )

        user = create_user(db, payload)

        token = create_token(user.id, user.username, user.role)

        auth_data = AuthDTO(
            username=user.username,
            role=user.role,
            token=token
        )

        return auth_data

    except HTTPException as e:
        logger.error(e)
        raise
    except Exception as e:
        logger.error(e)
        raise


def check_admin_role(token_payload: dict) -> bool:
    return True if token_payload["role"] == "admin" else False
