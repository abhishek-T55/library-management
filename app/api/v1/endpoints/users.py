from typing import Any, List
import json
from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.models import UserCreate, User, UserUpdate, UserPublic
import app.crud
from app.api.v1.deps import get_current_user
from app.api.v1.deps import SessionDep
import app.utils.cache

from app.utils.cache import redis_client
import app.utils
from app.utils.rate_limiting import limiter
from app.services.task_scheduler import send_registration_email

router = APIRouter()

@router.get("/{user_id}", dependencies=[Depends(get_current_user)], response_model=User)
def get_user_by_id(user_id: int, session: SessionDep):
    cached_user = redis_client.get(f"user: {user_id}")
    if cached_user:
        return json.loads(cached_user)
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    redis_client.setex(f"user: {user_id}", 60, json.dumps(db_user.model_dump()))
    return db_user


@router.get("/", dependencies=[Depends(get_current_user)], response_model=List[User])
@limiter.limit("10/minute")
def list_all_users(*, request:Request, session: SessionDep):
    db_users = app.crud.get_all_users(session=session)
    redis_client.setex("users", 60, json.dumps([user.model_dump() for user in db_users]))
    return db_users


@router.post(
    "/", dependencies=[Depends(get_current_user)], response_model=User
)
@limiter.limit("5/minute")
def create_user(*, request: Request, session: SessionDep, user_in: UserCreate) -> Any:
    user = app.crud.create_user(session=session, user_create=user_in)
    send_registration_email(user.email)
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