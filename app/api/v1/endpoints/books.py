from typing import Optional
from app.db.models import Book
from app.schemas.book import BookCreate
from fastapi import APIRouter, Request, Depends, Query
import app.crud
import json
from app.api.v1.deps import get_current_user
from app.api.v1.deps import SessionDep
from app.db.models import User
from app.schemas.book import BookResponse, BookFilter, Pagination
from app.exceptions import BookNotFoundException
import app.utils.cache
from typing import Any, List

from app.utils.cache import redis_client
import app.utils
from app.utils.rate_limiting import limiter

router = APIRouter()


@router.get("/filter", dependencies=[Depends(get_current_user)], response_model=List[Book])
def get_filtered_books(
    *,
    session: SessionDep,
    title: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    filters = BookFilter(title=title, owner_id=owner_id)
    pagination = Pagination(skip=skip, limit=limit)
    books = app.crud.get_filtered_books(session=session, filters=filters, pagination=pagination)
    return books


@router.get("/{book_id}", dependencies=[Depends(get_current_user)], response_model=BookResponse)
@limiter.limit("20/minute")
def get_book_by_id(request: Request, book_id: int, session: SessionDep):
    cached_book = redis_client.get(f"book: {book_id}")
    if cached_book:
        return json.loads(cached_book)
    db_book = session.get(Book, book_id)
    if not db_book:
        raise BookNotFoundException()
    redis_client.setex(f"book: {book_id}", 60, json.dumps(db_book.model_dump()))
    return db_book


@router.post("/", dependencies=[Depends(get_current_user)], response_model=Book)
def create_book(*, request: Request, session: SessionDep, book_in: BookCreate,  current_user: User = Depends(get_current_user)) -> Any:
    book = app.crud.create_book(session=session, book_create=book_in, owner_id=current_user.id)
    return book


@router.get("/", dependencies=[Depends(get_current_user)], response_model=List[BookResponse])
@limiter.limit("10/minute")
def list_all_books(*, request: Request, session: SessionDep):
    db_books = app.crud.get_all_books(session=session)
    redis_client.setex("books", 60, json.dumps([book.model_dump() for book in db_books]))
    return db_books


@router.delete("/{book_id}", dependencies=[Depends(get_current_user)], response_model=BookResponse)
def delete_book(book_id: int, session: SessionDep):
    book = app.crud.delete_book(session=session, book_id=book_id)
    if not book:
        raise BookNotFoundException()
    return book

@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    dependencies=[Depends(get_current_user)]
)
def update_book(
    *,
    session: SessionDep,
    book_id: int,
    book_in: BookCreate
) -> Any:
    db_book = session.get(Book, book_id)
    if not db_book:
        raise BookNotFoundException()
    db_book = app.crud.update_book(session=session, db_book=db_book, book_in=book_in)
    return db_book
