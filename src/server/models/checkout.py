from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CheckoutBase(BaseModel):
    class Config:
        from_attributes = True


class QRCodeDTO(CheckoutBase):
    id: int
    book_title: str
    user_full_name: str
    checkout_date: str
    pickup_code: int


class CheckoutDTO(CheckoutBase):
    id: int
    book_name: str
    checkout_date: datetime
    return_date: datetime


class CheckoutAdminDTO(CheckoutBase):
    id: int
    user_email: Optional[str]
    book_name: Optional[str]
    checkout_date: datetime
    return_date: datetime
    qr_code_data: Optional[QRCodeDTO]


class CheckoutAdminResponse(CheckoutBase):
    data: Optional[List[CheckoutAdminDTO]]


class CheckoutResponse(CheckoutBase):
    data: Optional[List[CheckoutDTO]]
