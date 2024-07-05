from app.db.models import BookCreate, Book, BookUpdate
from fastapi import APIRouter, HTTPException, Request, Depends
import app.crud
import json
from app.api.v1.deps import get_current_user
from app.api.v1.deps import SessionDep
from app.db.models import User
import app.utils.cache
from typing import Any, List

from app.utils.cache import redis_client
import app.utils
from app.utils.rate_limiting import limiter

router = APIRouter()


@router.get("/{book_id}", dependencies=[Depends(get_current_user)], response_model=Book)
@limiter.limit("20/minute")
def get_book_by_id(request: Request, book_id: int, session: SessionDep):
    cached_book = redis_client.get(f"book: {book_id}")
    if cached_book:
        return json.loads(cached_book)
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="The book with this id does not exist in the system",
        )
    redis_client.setex(f"book: {book_id}", 60, json.dumps(db_book.model_dump()))
    return db_book


@router.post("/", dependencies=[Depends(get_current_user)], response_model=Book)
def create_book(*, request: Request, session: SessionDep, book_in: BookCreate,  current_user: User = Depends(get_current_user)) -> Any:
    book = app.crud.create_book(session=session, book_create=book_in, owner_id=current_user.id)
    return book


@router.get("/", dependencies=[Depends(get_current_user)], response_model=List[Book])
@limiter.limit("10/minute")
def list_all_books(*, request: Request, session: SessionDep):
    db_books = app.crud.get_all_books(session=session)
    redis_client.setex("books", 60, json.dumps([book.model_dump() for book in db_books]))
    return db_books


@router.delete("/{book_id}", dependencies=[Depends(get_current_user)], response_model=Book)
def delete_book(book_id: int, session: SessionDep):
    book = app.crud.delete_book(session=session, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch(
    "/{book_id}",
    response_model=Book,
)
def update_book(
    *,
    session: SessionDep,
    book_id: int,
    book_in: BookUpdate
) -> Any:
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="The book with this id does not exist in the system",
        )
    db_book = app.crud.update_book(session=session, db_book=db_book, book_in=book_in)
    return db_book
