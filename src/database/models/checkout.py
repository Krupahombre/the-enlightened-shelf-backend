import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database import Base


class Checkout(Base):
    __tablename__ = "Checkout"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    book_id = Column(Integer, ForeignKey("Book.id"))
    checkout_date = Column(DateTime, default=datetime.datetime.now())
    return_date = Column(DateTime)

    book = relationship('Book', back_populates='checkouts')
    user = relationship('User', back_populates='checkouts')
