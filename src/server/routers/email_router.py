from fastapi import APIRouter, Query
from starlette import status

from src.server.models.checkout import QRCodeDTO
from src.utils.email_sender.sender import email_sender

router = APIRouter(
    prefix="/emails",
    tags=["Email"]
)


@router.post("/", status_code=status.HTTP_200_OK)
def send(email: str = Query()):
    qr_data = QRCodeDTO(
        id=1,
        book_title="Sample Book",
        user_full_name="John Doe",
        checkout_date="2023-01-01",
        pickup_code=12345
    )
    email_sender.send_email(email, qr_data)
