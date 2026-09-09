"""Authentication and User schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^[0-9+ -]{10,15}$")
    password: str = Field(..., min_length=6)
    preferred_language: str = "hi"


class UserLogin(BaseModel):
    email_or_phone: str
    password: str


class UserOut(BaseModel):
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    preferred_language: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
