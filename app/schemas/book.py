from pydantic import BaseModel, field_validator
from typing import Optional


class BookBase(BaseModel):
    title: str
    description: str = None
    url: str


class BookCreate(BookBase):
    title: str

    @field_validator("url")
    def validate_http_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class BookUpdate(BookBase):
    title: str = None
    description: str = None
    url: str = None


class BookResponse(BookBase):
    id: int
    title: str
    description: str | None
    url: str | None

    class Config:
        from_attributes = True


class BookFilter(BaseModel):
    title: Optional[str] = None
    owner_id: Optional[int] = None


class Pagination(BaseModel):
    skip: int = 0
    limit: int = 0
