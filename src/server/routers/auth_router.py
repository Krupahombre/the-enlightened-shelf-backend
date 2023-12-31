from fastapi import APIRouter
from starlette import status

from src.database.database import db_dependency
from src.server.models.auth import AuthResponse, LoginPayload, RegisterPayload
from src.service.auth_service import login_user, register_user
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(db: db_dependency, payload: LoginPayload):
    return AuthResponse(data=login_user(db, payload))


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(db: db_dependency, payload: RegisterPayload):
    return AuthResponse(data=register_user(db, payload))


@router.get("/test_auth", status_code=status.HTTP_200_OK)
def test_get(token: token_dependency):
    return token
