from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.session import engine

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{config.API_V1_STR}/login/access-token"
# )


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
# TokenDep = Annotated[str, Depends(reusable_oauth2)]
