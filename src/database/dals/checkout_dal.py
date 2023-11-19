from typing import Type

from sqlalchemy.orm import Session

from src.database import Checkout


def get_checkouts_admin(db: Session) -> list[Type[Checkout]] | None:
    return db.query(Checkout).order_by(Checkout.checkout_date).all()


def get_checkouts_by_user_id(db: Session, user_id: int) -> list[Type[Checkout]] | None:
    return db.query(Checkout).filter(Checkout.user_id == user_id).order_by(Checkout.checkout_date).all()


def save_checkout(db: Session, checkout_model: Checkout) -> None:
    db.add(checkout_model)
    db.commit()
