from typing import Optional, List

from pydantic import BaseModel


class BookBase(BaseModel):
    class Config:
        from_attributes = True


class BookDTO(BookBase):
    id: int
    title: str
    author: str
    description: str
    quantity: int
    quantity_available: int
    category: str
    img: str


class BookPayload(BaseModel):
    title: str
    author: str
    description: str
    quantity: int
    category: str
    img: str


class BookUpdatePayload(BaseModel):
    quantity: int
    quantity_available: int


class BookResponse(BookBase):
    data: Optional[List[BookDTO]]


class BookSingleResponse(BookBase):
    data: Optional[BookDTO]
