from pydantic import BaseModel, HttpUrl


class BookBase(BaseModel):
    title: str
    description: str = None
    url: str


class BookCreate(BookBase):
    title: str


class BookUpdate(BookBase):
    title: str = None
    description: str = None
    url: HttpUrl = None


class BookResponse(BookBase):
    id: int
    title: str
    description: str | None
    url: str | None

    class Config:
        from_attributes = True
