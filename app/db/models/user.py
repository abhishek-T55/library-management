from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=200)
    is_locked: bool = False
    full_name: str | None = Field(default=None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=20)
    full_name: str | None = Field(default=None, max_length=200)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=200)
    password: str | None = Field(default=None, min_length=8, max_length=20)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=200)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    # items: list["Book"] = Relationship(back_populates="owner")
