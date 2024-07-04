from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    phone_number: str
    email: str
    created_at: datetime
    updated_at: datetime