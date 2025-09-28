from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserAdd(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None


class LogIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    expires_in: int
