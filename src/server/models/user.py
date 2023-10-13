from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    class Config:
        from_attributes = True


class UserDTO(UserBase):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


class UserResponse(UserBase):
    data: Optional[UserDTO]
