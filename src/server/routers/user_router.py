from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.user import UserResponse
from src.service.user_service import get_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(db: db_dependency, user_id: int = Path(gt=0)):
    return UserResponse(data=get_user(db, user_id))
