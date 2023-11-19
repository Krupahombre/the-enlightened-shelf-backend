from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CheckoutBase(BaseModel):
    class Config:
        from_attributes = True


class CheckoutAdminDTO(CheckoutBase):
    id: int
    user_full_name: Optional[str]
    book_name: Optional[str]
    checkout_date: datetime
    return_date: datetime
    qr_code_data: str


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
