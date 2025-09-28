from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CreatePermission(BaseModel):
    code: str


class AssignPermission(BaseModel):
    permission_code: str
    role_code: str
