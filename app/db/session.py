from sqlmodel import Session, create_engine

from app.core.config import config

engine = create_engine(str(config.database.url))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    print("database initialized")
