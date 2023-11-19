from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.checkout import CheckoutAdminResponse, CheckoutAdminResponseImage
from src.service.checkout_service import get_checkouts_list_admin, get_file, create_checkout
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/checkouts",
    tags=["Checkout"]
)


@router.get("/", response_model=CheckoutAdminResponse, status_code=status.HTTP_200_OK)
def get_checkouts_list_secured(token: token_dependency, db: db_dependency):
    return CheckoutAdminResponse(data=get_checkouts_list_admin(token, db))


@router.post("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_new_checkout(token: token_dependency, db: db_dependency, book_id: int = Path()):
    create_checkout(token, db, book_id)


@router.get('/image')
def get_image(token: token_dependency, db: db_dependency):
    return CheckoutAdminResponseImage(data=get_file(token, db))
