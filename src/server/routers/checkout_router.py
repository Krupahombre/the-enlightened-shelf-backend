from fastapi import APIRouter
from starlette import status

from src.database.database import db_dependency
from src.server.models.checkout import CheckoutAdminResponse
from src.service.checkout_service import get_checkouts_list_admin, get_file
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/checkouts",
    tags=["Checkout"]
)


@router.get("/", response_model=CheckoutAdminResponse, status_code=status.HTTP_200_OK)
def get_checkouts_list_secured(token: token_dependency, db: db_dependency):
    return CheckoutAdminResponse(data=get_checkouts_list_admin(token, db))


@router.get('/image')
def get_image(token: token_dependency, db: db_dependency):
    return CheckoutAdminResponse(data=get_file(token, db))
