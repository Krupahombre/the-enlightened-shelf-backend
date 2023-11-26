from fastapi import APIRouter, Path
from starlette import status

from src.database.database import db_dependency
from src.server.models.checkout import CheckoutAdminResponse, CheckoutResponse
from src.service.checkout_service import get_checkouts_list_admin, create_checkout, get_checkouts_list, extend_loan, \
    return_book
from src.utils.token_utils import token_dependency

router = APIRouter(
    prefix="/checkouts",
    tags=["Checkout"]
)


@router.get("/", response_model=CheckoutAdminResponse, status_code=status.HTTP_200_OK)
def get_checkouts_list_secured(token: token_dependency, db: db_dependency):
    return CheckoutAdminResponse(data=get_checkouts_list_admin(token, db))


@router.get("/user", response_model=CheckoutResponse, status_code=status.HTTP_200_OK)
def get_user_checkout_list(token: token_dependency, db: db_dependency):
    return CheckoutResponse(data=get_checkouts_list(token, db))


@router.post("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_new_checkout(token: token_dependency, db: db_dependency, book_id: int = Path()):
    create_checkout(token, db, book_id)


@router.put("/extend-loan/{checkout_id}", status_code=status.HTTP_202_ACCEPTED)
def extend_loan_period(token: token_dependency, db: db_dependency, checkout_id: int = Path()):
    extend_loan(token, db, checkout_id)


@router.delete("/return/{checkout_id}", status_code=status.HTTP_204_NO_CONTENT)
def return_checked_out_book(token: token_dependency, db: db_dependency, checkout_id: int = Path()):
    return_book(token, db, checkout_id)
