import random
from datetime import datetime

from src.database import User, Book
from src.server.models.checkout import QRCodeDTO


def create_qr_data(user: User, book: Book, checkout_date: str) -> str:
    user_full_name = user.first_name + " " + user.last_name
    pickup_code = random.randint(100, 999)
    qr_data = str(
        book.title + ","
        + user_full_name + ","
        + str(checkout_date) + ","
        + str(pickup_code))
    return qr_data


def create_qr_code_dto(checkout_id: int, qr_code_data: str) -> QRCodeDTO:
    parts = qr_code_data.split(',')

    if len(parts) == 4:
        qr_code_dto = QRCodeDTO(
            id=checkout_id,
            book_title=parts[0],
            user_full_name=parts[1],
            checkout_date=parts[2],
            pickup_code=int(parts[3])
        )
        return qr_code_dto
    else:
        raise ValueError("Invalid QR code data format")
