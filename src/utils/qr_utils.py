import random

from src.database import User, Book


def create_qr_data(user: User, book: Book, checkout_date: str) -> str:
    user_full_name = user.first_name + " " + user.last_name
    pickup_code = random.randint(100, 999)
    qr_data = str(
        book.title + ","
        + user.email + ","
        + user_full_name + ","
        + str(checkout_date) + ","
        + str(pickup_code))
    return qr_data
