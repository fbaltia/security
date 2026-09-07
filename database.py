import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import String, create_engine
from sqlalchemy.orm import  Session, mapped_column, sessionmaker

from models.base import Base

load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL is not configured. Add it to the .env file.')
    return database_url



engine = create_engine(get_database_url(), pool_pre_ping=True)
local_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = local_session()
    try:
        yield session
    finally:
        session.close()