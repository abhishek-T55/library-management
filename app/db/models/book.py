from sqlmodel import Field, SQLModel, Relationship, AutoString
from typing import Optional
from pydantic import AnyUrl


class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    url: AnyUrl | None = Field(default=None, sa_type=AutoString)


class BookCreate(BookBase):
    title: str = Field(min_length=1, max_length=255)


class BookUpdate(BookBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: "User" = Relationship(back_populates="books")
