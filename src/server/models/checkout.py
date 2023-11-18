from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile
from pydantic import BaseModel
from starlette.responses import FileResponse


class CheckoutBase(BaseModel):
    class Config:
        from_attributes = True


class CheckoutAdminDTO(CheckoutBase):
    id: int
    # user_id: int
    # book_id: int
    user_full_name: Optional[str]
    book_name: Optional[str]
    checkout_date: datetime
    return_date: datetime
    qr_code: Optional[str]


class CheckoutAdminResponse(CheckoutBase):
    data: Optional[List[CheckoutAdminDTO]]
