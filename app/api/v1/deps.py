from collections.abc import Generator
from typing import Annotated
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.config import config
from app.core import security
from app.db.models import User, TokenPayload
from pydantic import ValidationError

from app.db.session import engine

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, config.secret_key, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_locked:
        raise HTTPException(status_code=400, detail="Locked user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
