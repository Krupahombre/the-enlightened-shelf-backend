import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.dals.user_dal import get_user_by_id
from src.server.models.user import UserDTO

logger = logging.getLogger("UserService")


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
