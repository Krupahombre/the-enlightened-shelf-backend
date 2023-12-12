from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CheckoutBase(BaseModel):
    class Config:
        from_attributes = True


class CheckoutHistoryDTO(CheckoutBase):
    id: int
    book_title: str
    book_id: int
    checkout_date: datetime
    return_date: datetime


class CheckoutHistoryResponse(CheckoutBase):
    data: Optional[List[CheckoutHistoryDTO]]
