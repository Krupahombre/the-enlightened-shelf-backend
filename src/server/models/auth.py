from typing import Optional

from pydantic import BaseModel


class AuthBase(BaseModel):
    class Config:
        from_attributes = True


class AuthDTO(AuthBase):
    username: str
    role: str
    token: str


class LoginPayload(BaseModel):
    username: str
    password: str


class AuthResponse(AuthBase):
    data: Optional[AuthDTO]
