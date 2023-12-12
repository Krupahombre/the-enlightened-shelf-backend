from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.database.models.checkout_history import CheckoutHistory


def get_checkouts_history_by_user_id(db: Session, user_id: int) -> list[Type[CheckoutHistory]] | None:
    return (db.query(CheckoutHistory)
            .filter(CheckoutHistory.user_id == user_id)
            .order_by(desc(CheckoutHistory.checkout_date))
            .all())


def save_checkout_history(db: Session, checkout_history_model: CheckoutHistory) -> None:
    db.add(checkout_history_model)
    db.commit()
