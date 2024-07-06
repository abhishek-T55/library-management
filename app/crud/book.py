from typing import Any, List
from sqlmodel import Session, select
from sqlalchemy.sql import func
from app.db.models import Book, BookCreate, BookUpdate
from app.schemas.book import BookResponse, BookFilter, Pagination
from app.exceptions import BookNotFoundException

def get_all_books(*, session: Session) -> List[BookResponse]:
    books = session.exec(select(Book)).all()
    return books

def get_filtered_books(
    *,
    session: Session,
    filters: BookFilter,
    pagination: Pagination
) -> List[BookResponse]:
    query = select(Book)
    if filters.title:
        # TODO: implement sql ilike operator
        query = query.where(func.lower(Book.title) == func.lower(filters.title))

    if filters.owner_id:
        query = query.where(Book.owner_id == filters.owner_id)

    query = query.offset(pagination.skip).limit(pagination.limit)

    books = session.exec(query).all()
    return books

def create_book(*, session: Session, book_create: BookCreate, owner_id: int) -> BookResponse:
    db_book = Book.model_validate(book_create)
    db_book.owner_id = owner_id
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

def delete_book(*, session: Session, book_id: int) -> Any:
    db_book = session.get(Book, book_id)
    if not db_book:
        raise BookNotFoundException()
    session.delete(db_book)
    session.commit()
    return db_book

def update_book(*, session: Session, db_book: Book, book_in: BookUpdate) -> Any:
    book_data = book_in.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book
