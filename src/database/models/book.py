from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Book(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    quantity_available = Column(Integer)
    category = Column(String)
    img = Column(String)
