from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CheckoutBase(BaseModel):
    class Config:
        from_attributes = True


class QRCodeDTO(BaseModel):
    id: int
    book_title: str
    user_full_name: str
    checkout_date: str
    pickup_code: int


class CheckoutAdminDTO(CheckoutBase):
    id: int
    user_email: Optional[str]
    book_name: Optional[str]
    checkout_date: datetime
    return_date: datetime
    qr_code_data: Optional[QRCodeDTO]


class CheckoutAdminDTOImage(CheckoutBase):
    id: int
    user_full_name: Optional[str]
    book_name: Optional[str]
    checkout_date: datetime
    return_date: datetime
    qr_code: Optional[str]


class CheckoutAdminResponse(CheckoutBase):
    data: Optional[List[CheckoutAdminDTO]]


class CheckoutAdminResponseImage(CheckoutBase):
    data: Optional[List[CheckoutAdminDTO]]
