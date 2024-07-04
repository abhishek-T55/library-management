from typing import Any
from fastapi import APIRouter, HTTPException
from app.db.models import UserCreate, User, UserUpdate
import app.crud
from app.api.v1.deps import SessionDep


router = APIRouter()

@router.post(
    "/", response_model=User
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    user = app.crud.create_user(session=session, user_create=user_in)
    return user


@router.patch(
    "/{user_id}",
    response_model=User,
)
def update_user(
    *,
    session: SessionDep,
    user_id: int,
    user_in: UserUpdate,
) -> Any:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    db_user = app.crud.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user