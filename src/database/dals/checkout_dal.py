from typing import Type

from sqlalchemy.orm import Session

from src.database import Checkout


def get_checkouts_admin(db: Session) -> list[Type[Checkout]] | None:
    return db.query(Checkout).order_by(Checkout.checkout_date).all()


def save_checkout(db: Session, checkout_model: Checkout) -> None:
    db.add(checkout_model)
    db.commit()
