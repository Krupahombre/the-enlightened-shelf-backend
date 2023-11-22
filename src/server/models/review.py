from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ReviewBase(BaseModel):
    class Config:
        from_attributes = True


class ReviewPayload(BaseModel):
    rating: float
    comment: str


class ReviewDTO(ReviewBase):
    id: int
    username: str
    date: datetime
    rating: float
    comment: str


class ReviewResponse(ReviewBase):
    data: Optional[List[ReviewDTO]]
