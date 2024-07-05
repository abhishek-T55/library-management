from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    email: EmailStr
    is_locked: bool = False
    full_name: str | None


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 8 or len(v) > 20:
            raise ValueError("Password must be between 8 and 20 characters")
        return v

    @field_validator("full_name")
    def full_name_length(cls, v):
        if v and len(v) > 100:
            raise ValueError("Full name must be less than 100 characters")
        return v


class UserUpdate(UserBase):
    email: EmailStr = None
    password: str = None


class UserResponse(UserBase):
    id: int
    full_name: str | None
    email: EmailStr

    class Config:
        from_attributes = True


class UserBookCountResponse(UserResponse):
    total_books: int | None
