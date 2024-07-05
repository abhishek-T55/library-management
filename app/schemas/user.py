from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_locked: bool = False
    full_name: str | None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr = None
    password: str = None


class UserResponse(UserBase):
    id: int
    full_name: str | None
    email: EmailStr

    class Config:
        from_attributes = True