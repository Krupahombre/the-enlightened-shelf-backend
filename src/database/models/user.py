from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    role = Column(String, default="user")

    reviews = relationship('Review', back_populates='user')
    checkouts = relationship('Checkout', back_populates='user')
    checkouts_history = relationship('CheckoutHistory', back_populates='user')
