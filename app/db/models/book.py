from sqlmodel import Field, SQLModel

class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class BookCreate(BookBase):
    title: str = Field(min_length=1, max_length=255)


class BookUpdate(BookBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    # owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    # owner: User | None = Relationship(back_populates="books")
