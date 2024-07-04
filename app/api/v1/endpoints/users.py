from typing import Any
from fastapi import APIRouter
from app.db.models import UserCreate, User
import app.crud
from app.api.v1.deps import SessionDep


router = APIRouter()

@router.post(
    "/", response_model=User
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    user = app.crud.create_user(session=session, user_create=user_in)
    return user