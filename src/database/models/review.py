import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship

from src.database.database import Base


class Review(Base):
    __tablename__ = "Review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    book_id = Column(Integer, ForeignKey("Book.id"))
    date = Column(DateTime, default=datetime.datetime.now())
    rating = Column(Float)
    comment = Column(String)

    book = relationship('Book', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
