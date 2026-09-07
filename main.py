from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import User, create_tables, get_session
from utils import jwt_utils, password_utils


load_dotenv()

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * from User"))
        print(result.fetchall())
        