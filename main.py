from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import create_tables, local_session
from models.user import User
from utils import jwt_utils, password_utils


load_dotenv()

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    
    create_tables()

    
    with local_session() as session:
        user = User(
            username="duh",
            email="doh@duh.com",
            role = "ZZZ",
            password_hash=""
        )
        user.set_password("MonMotDePasse123")
        session.add(user)
        session.commit()
    print(user.id)

