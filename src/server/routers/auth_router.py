from fastapi import APIRouter
from starlette import status

from src.database.database import db_dependency
from src.server.models.auth import AuthResponse, LoginPayload, RegisterPayload
from src.service.auth_service import login_user, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(db: db_dependency, payload: LoginPayload):
    return AuthResponse(data=login_user(db, payload))


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(db: db_dependency, payload: RegisterPayload):
    register_user(db, payload)
