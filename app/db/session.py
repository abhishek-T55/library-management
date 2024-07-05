from sqlmodel import Session, create_engine

from app.core.config import config

engine = create_engine(str(config.database.url))

def init_db(session: Session) -> None:
    pass
