from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.models import UserCreate, User, UserUpdate, UserPublic
import app.crud
from app.api.v1.deps import get_current_user
from app.api.v1.deps import SessionDep

from app.utils.rate_limiting import limiter


router = APIRouter()

@router.get("/{user_id}", dependencies=[Depends(get_current_user)], response_model=User)
def get_user_by_id(user_id: int, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return db_user


@router.get("/", dependencies=[Depends(get_current_user)], response_model=List[User])
@limiter.limit("10/minute")
def list_all_users(*, request:Request, session: SessionDep):
    return app.crud.get_all_users(session=session)


@router.post(
    "/", dependencies=[Depends(get_current_user)], response_model=User
)
@limiter.limit("2/minute")
def create_user(*, request: Request, session: SessionDep, user_in: UserCreate) -> Any:
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


@router.delete("/{user_id}" ,dependencies=[Depends(get_current_user)], response_model=UserPublic)
def delete_user(user_id: int, session: SessionDep):
    user = app.crud.delete_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user